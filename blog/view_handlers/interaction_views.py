import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.utils.text import slugify

from blog.forms import BugReportForm, CommentForm
from blog.models import Comment, Follow, Like, Notification, PollOption, PollVote, Post, QuizAnswer, QuizOption
from blog.services import ANONYMOUS_COMMENT_USERNAME, are_users_blocked, get_allow_anonymous_comments, get_blog_preferences, is_user_restricted, publish_due_posts
from blog.comment_rate_limit import check_comment_allowed, remember_comment_sent
from blog.security import log_security_event


# BLOGPLATFORM_MENTION_NOTIFICATIONS_START
def _bp_extract_mentioned_usernames(content):
    import re

    if not content:
        return []

    found = re.findall(r"(?<!\w)@([A-Za-z0-9_.+-]{2,150})", str(content))
    usernames = []

    for username in found:
        username = username.strip(".,!?;:()[]{}<>\"'")

        if not username:
            continue

        if username.lower() not in [item.lower() for item in usernames]:
            usernames.append(username)

    return usernames[:20]


def _create_mention_notifications(comment):
    if not comment:
        return

    if getattr(comment, "is_anonymous", False):
        return

    if not getattr(comment, "author_id", None):
        return

    mentioned_usernames = _bp_extract_mentioned_usernames(comment.content)

    if not mentioned_usernames:
        return

    for username in mentioned_usernames:
        mentioned_user = User.objects.filter(username__iexact=username, is_active=True).first()

        if not mentioned_user:
            continue

        if mentioned_user.id == comment.author_id:
            continue

        Notification.objects.get_or_create(
            recipient=mentioned_user,
            sender=comment.author,
            post=comment.post,
            comment=comment,
            notification_type="mention",
        )
# BLOGPLATFORM_MENTION_NOTIFICATIONS_END

# BLOGPLATFORM_INTERACTION_COMMENT_ANCHOR_URLS_START
def _bp_post_public_slug(post):
    slug = slugify(getattr(post, "title", "") or "", allow_unicode=False).strip("-")
    return slug or f"post-{post.pk}"


def _bp_post_public_url(post):
    return reverse("post_detail_slug", args=[post.pk, _bp_post_public_slug(post)])


def _bp_comment_public_url(comment):
    return f"{_bp_post_public_url(comment.post)}#comment-{comment.pk}"
# BLOGPLATFORM_INTERACTION_COMMENT_ANCHOR_URLS_END

@require_POST
def create_comment(request, pk):
    publish_due_posts()
    post = get_object_or_404(Post, pk=pk)
    blog_preferences = get_blog_preferences(post.author)
    allow_anonymous_comments = get_allow_anonymous_comments(post.author)

    if request.user.is_authenticated and are_users_blocked(request.user, post.author):
        messages.error(request, 'Ne možeš komentirati (blokiranje).')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    if request.user.is_authenticated and is_user_restricted(post.author, request.user):
        messages.error(request, 'Autor te je ograničio pa ne možeš komentirati.')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    if not blog_preferences.get('allow_comments', True) or not post.allow_comments:
        messages.error(request, 'Komentari su isključeni za ovaj post.')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    if request.method == 'POST':
        content = (request.POST.get('content') or '').strip()
        wants_anonymous = request.POST.get('anonymous') in {'on', '1', 'true'}
        if not request.user.is_authenticated:
            messages.error(request, 'Za komentiranje je potrebna registracija.')
            return redirect('login')

        if wants_anonymous and not allow_anonymous_comments:
            messages.error(request, 'Anonimno komentiranje nije dopušteno za ovaj blog.')
            return redirect(_bp_post_public_url(post))

        is_anonymous_comment = bool(wants_anonymous and allow_anonymous_comments)

        if content:
            allowed, error_message = check_comment_allowed(request, post, content)
            if not allowed:
                event_type = 'duplicate_comment_blocked' if 'isti komentar' in error_message.lower() else 'comment_rate_limited'
                log_security_event(
                    request,
                    event_type=event_type,
                    severity='warning',
                    message=error_message,
                    metadata={'post_id': post.id, 'post_author': post.author.username},
                )
                messages.error(request, error_message)
                return redirect(_bp_comment_public_url(comment))

            comment = Comment.objects.create(
                post=post,
                author=request.user,
                content=content,
                is_anonymous=is_anonymous_comment,
            )
            remember_comment_sent(request, post, content)
            _create_mention_notifications(comment)
            if request.user.is_authenticated and not is_anonymous_comment and request.user != post.author:
                Notification.objects.create(recipient=post.author, sender=request.user, post=post, comment=comment, notification_type='comment')

    return redirect(_bp_comment_public_url(comment))


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    post = comment.post
    post_id = post.id
    if request.method == 'POST':
        comment.delete()
        return redirect(_bp_post_public_url(post))
    return render(request, 'blog/delete_comment.html', {'comment': comment})


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(_bp_comment_public_url(comment))
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/edit_comment.html', {'form': form})


@login_required
@require_POST
def like_post(request, post_id):
    publish_due_posts()

    post = get_object_or_404(Post, id=post_id, status='published')

    redirect_url = (
        request.POST.get('next')
        or request.META.get('HTTP_REFERER')
        or reverse('post_detail', args=[post.id])
    )

    if are_users_blocked(request.user, post.author):
        messages.error(request, 'Ne možeš lajkati ovaj post (blokiranje).')
        return redirect(redirect_url)

    if is_user_restricted(post.author, request.user):
        messages.error(request, 'Autor te je ograničio pa ne možeš lajkati postove.')
        return redirect(redirect_url)

    existing_like = Like.objects.filter(user=request.user, post=post).first()

    if existing_like:
        existing_like.delete()
    else:
        Like.objects.create(user=request.user, post=post)

        if request.user != post.author:
            Notification.objects.get_or_create(
                recipient=post.author,
                sender=request.user,
                post=post,
                notification_type='like',
            )

    return redirect(redirect_url)

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            log_security_event(
                request,
                event_type='password_change_success',
                user=user,
                severity='warning',
                message='Korisnik je uspješno promijenio lozinku.',
            )
            messages.success(request, 'Lozinka je uspješno promijenjena.')
            return redirect('password_change')
        log_security_event(
            request,
            event_type='password_change_failed',
            severity='warning',
            message='Neuspješna promjena lozinke.',
            metadata={'errors': form.errors.get_json_data()},
        )
        messages.error(request, 'Molimo ispravite greške ispod.')
    else:
        form = PasswordChangeForm(request.user)

    for field in form.fields.values():
        field.widget.attrs.update({'class': 'form-control'})
    return render(request, 'blog/password_change.html', {'form': form})


@login_required
def notifications(request):
    notifications_qs = request.user.notifications.all().order_by('-created_at')
    notifications_qs.filter(is_read=False).update(is_read=True)
    return render(request, 'blog/notifications.html', {'notifications': notifications_qs})


@login_required
def notification_redirect(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()

    if notification.notification_type == 'follow':
        return redirect('user_blog', username=notification.sender.username)
    if notification.notification_type == 'like':
        return redirect(_bp_post_public_url(notification.post))
    if notification.notification_type == 'mention' and notification.post_id:
        if notification.comment_id:
            return redirect(f"{_bp_post_public_url(notification.post)}#comment-{notification.comment.id}")
        return redirect(_bp_post_public_url(notification.post))
    if notification.notification_type == 'comment':
        return redirect(f"{_bp_post_public_url(notification.post)}#comment-{notification.comment.id}")
    return redirect('home')


@login_required
@require_POST
def delete_avatar(request):
    profile = request.user.profile
    if profile.avatar:
        profile.avatar.delete(save=False)
        profile.avatar = None
        profile.save()
        log_security_event(
            request,
            event_type='avatar_deleted',
            user=request.user,
            severity='info',
            message='Korisnik je izbrisao avatar.',
        )
    return redirect('blog_settings')


@login_required
@require_POST
def quiz_answer(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published', post_type='quiz')
    if are_users_blocked(request.user, post.author):
        messages.error(request, 'Ne možeš odgovoriti na kviz (blokiranje).')
        return redirect('post_detail', post_id=post.id)
    if QuizAnswer.objects.filter(post=post, user=request.user).exists():
        return redirect('post_detail', post_id=post.id)
    if request.method == 'POST':
        option = QuizOption.objects.filter(id=request.POST.get('option'), post=post).first()
        if option:
            QuizAnswer.objects.create(post=post, user=request.user, selected_option=option)
    return redirect('post_detail', post_id=post.id)


@login_required
@require_POST
def poll_vote(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published', post_type='poll')
    if are_users_blocked(request.user, post.author):
        messages.error(request, 'Ne možeš glasati (blokiranje).')
        return redirect('post_detail', post_id=post.id)
    if PollVote.objects.filter(post=post, user=request.user).exists():
        return redirect('post_detail', post_id=post.id)
    if request.method == 'POST':
        option = PollOption.objects.filter(id=request.POST.get('option'), post=post).first()
        if option:
            PollVote.objects.create(post=post, user=request.user, option=option)
    return redirect('post_detail', post_id=post.id)


@require_POST
def submit_bug_report(request):
    form = BugReportForm(request.POST)
    request_type = (request.POST.get('request_type') or 'kvar').strip().lower()
    request_type_map = {
        'kvar': ('bug', 'KVAR', 'Kvar je prijavljen.'),
        'pitanje': ('question', 'PITANJE', 'Pitanje je poslano.'),
        'prijedlog': ('idea', 'PRIJEDLOG', 'Prijedlog je poslan.'),
    }
    request_value, request_label, success_message = request_type_map.get(request_type, request_type_map['kvar'])
    email = (request.POST.get('email') or '').strip()
    page_url = (request.META.get('HTTP_REFERER') or '').strip()

    if form.is_valid():
        bug = form.save(commit=False)
        if request.user.is_authenticated:
            bug.user = request.user

        bug.request_type = request_value
        if hasattr(bug, 'email'):
            bug.email = email
        if hasattr(bug, 'page_url') and page_url:
            bug.page_url = page_url

        raw_title = (bug.title or '').strip()
        prefixed_title = raw_title if raw_title.startswith('[') else f'[{request_label}] {raw_title}'
        bug.title = prefixed_title

        base_description = (bug.description or '').strip()
        info_lines = []
        if email:
            info_lines.append(f'Kontakt email: {email}')
        if page_url:
            info_lines.append(f'Stranica: {page_url}')
        if request.user.is_authenticated:
            info_lines.append(f'Korisnik: {request.user.username}')
        else:
            info_lines.append('Korisnik: anonimno')

        full_description = base_description
        if info_lines:
            full_description = f"{base_description}\n\n" + "\n".join(info_lines)
        bug.description = full_description

        bug.save()

        try:
            recipient = getattr(settings, 'BUG_REPORT_EMAIL', getattr(settings, 'DEFAULT_FROM_EMAIL', None))
            message = EmailMessage(
                subject=prefixed_title,
                body=full_description,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
                to=[recipient] if recipient else [],
                reply_to=[email] if email else None,
            )
            message.send(fail_silently=False)
        except Exception as exc:
            messages.warning(request, f'Poruka je spremljena, ali mail nije poslan: {exc}')
            return redirect(request.META.get('HTTP_REFERER', 'home'))

        messages.success(request, success_message)
    else:
        messages.error(request, 'Nije poslano. Provjeri polja i pokušaj opet.')
    return redirect(request.META.get('HTTP_REFERER', 'home'))
