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

from blog.forms import BugReportForm, CommentForm
from blog.models import Comment, Follow, Like, Notification, PollOption, PollVote, Post, QuizAnswer, QuizOption
from blog.services import ANONYMOUS_COMMENT_USERNAME, are_users_blocked, get_allow_anonymous_comments, get_blog_preferences, is_user_restricted, publish_due_posts
from blog.comment_rate_limit import check_comment_allowed, remember_comment_sent
from blog.security import log_security_event


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
        is_anonymous_comment = allow_anonymous_comments and (wants_anonymous or not request.user.is_authenticated)

        if not request.user.is_authenticated and not is_anonymous_comment:
            return redirect('login')

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
                return redirect(request.META.get('HTTP_REFERER') or reverse('user_blog', args=[post.author.username]))

            if is_anonymous_comment:
                anonymous_user, _ = User.objects.get_or_create(
                    username=ANONYMOUS_COMMENT_USERNAME,
                    defaults={'email': 'anon-comment@example.com'}
                )
                author = anonymous_user
            else:
                author = request.user

            comment = Comment.objects.create(post=post, author=author, content=content)
            remember_comment_sent(request, post, content)
            if request.user.is_authenticated and not is_anonymous_comment and request.user != post.author:
                Notification.objects.create(recipient=post.author, sender=request.user, post=post, comment=comment, notification_type='comment')

    return redirect(request.META.get('HTTP_REFERER') or reverse('user_blog', args=[post.author.username]))


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    post_id = comment.post.id
    if request.method == 'POST':
        comment.delete()
        return redirect('post_detail', post_id=post_id)
    return render(request, 'blog/delete_comment.html', {'comment': comment})


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/edit_comment.html', {'form': form})


@login_required
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if are_users_blocked(request.user, post.author):
        messages.error(request, 'Ne možeš lajkati ovaj post (blokiranje).')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    if is_user_restricted(post.author, request.user):
        messages.error(request, 'Autor te je ograničio pa ne možeš lajkati postove.')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if created:
        if request.user != post.author:
            Notification.objects.create(recipient=post.author, sender=request.user, post=post, notification_type='like')
    else:
        like.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))


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
        return redirect('post_detail', post_id=notification.post.id)
    if notification.notification_type == 'comment':
        return redirect(f"{reverse('post_detail', args=[notification.post.id])}#comment-{notification.comment.id}")
    return redirect('home')


@login_required
@require_POST
def delete_avatar(request):
    profile = request.user.profile
    if profile.avatar:
        if profile.avatar.path and os.path.isfile(profile.avatar.path):
            os.remove(profile.avatar.path)
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
