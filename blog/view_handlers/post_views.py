import hashlib
from django.contrib import messages
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from blog.forms import CommentForm, PostForm
from blog.analytics import build_live_analytics_context, build_tracking_context
from blog.models import Category, Comment, Notification, Post, PostImage, UserBox
from blog.services import (
    ANONYMOUS_COMMENT_USERNAME,
    apply_blog_preferences_to_profile,
    apply_tags_to_post,
    build_archives_for_user,
    build_calendar_for_user,
    build_month_navigation_urls,
    enrich_posts_with_quiz_poll_data,
    get_allow_anonymous_comments,
    build_author_profile_items,
    has_public_author_content,
    is_user_restricted,
    publish_due_posts,
    get_post_publication_datetime,
    resolve_design_template_name,
)
from blog.constants import MONTHS_HR
from blog.comment_rate_limit import check_comment_allowed, remember_comment_sent
from blog.security import log_security_event



# BLOGPLATFORM_POST_COMMENT_ANCHOR_URLS_START
def _bp_post_public_slug(post):
    slug = slugify(getattr(post, "title", "") or "", allow_unicode=False).strip("-")
    return slug or f"post-{post.pk}"


def _bp_post_public_url(post):
    return reverse("post_detail_slug", args=[post.pk, _bp_post_public_slug(post)])


def _bp_comment_public_url(comment):
    return f"{_bp_post_public_url(comment.post)}#comment-{comment.pk}"
# BLOGPLATFORM_POST_COMMENT_ANCHOR_URLS_END

POST_VIEW_COOLDOWN_SECONDS = 60 * 60 * 12

BOT_USER_AGENT_PARTS = (
    "bot",
    "crawl",
    "spider",
    "slurp",
    "facebookexternalhit",
    "whatsapp",
    "telegrambot",
    "discordbot",
    "linkedinbot",
    "preview",
    "python-requests",
    "curl",
    "wget",
)


def _get_client_ip(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


def _is_probably_bot(request):
    user_agent = (request.META.get("HTTP_USER_AGENT") or "").lower()
    if not user_agent:
        return True
    return any(part in user_agent for part in BOT_USER_AGENT_PARTS)


def _should_count_post_view(request, post):
    if request.method != "GET":
        return False

    if _is_probably_bot(request):
        return False

    if request.user.is_authenticated:
        if request.user == post.author:
            return False
        if request.user.is_staff or request.user.is_superuser:
            return False

    return True


def _post_view_cache_key(request, post):
    if request.user.is_authenticated:
        viewer_key = f"user:{request.user.pk}"
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key

        ip = _get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        raw_key = f"anon:{session_key}:{ip}:{user_agent}"
        viewer_key = hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

    return f"post-view:{post.pk}:{viewer_key}"


def _count_post_view(request, post):
    if not _should_count_post_view(request, post):
        return

    cache_key = _post_view_cache_key(request, post)

    if not cache.add(cache_key, True, POST_VIEW_COOLDOWN_SECONDS):
        return

    Post.objects.filter(pk=post.pk).update(views=F("views") + 1)
    post.views = (post.views or 0) + 1
def _apply_submit_action_to_post(post, submit_action, publish_at):
    if submit_action == 'draft':
        post.status = 'draft'
        post.publish_at = None
    elif publish_at:
        post.status = 'scheduled'
        post.publish_at = publish_at
    else:
        post.status = 'published'
        post.publish_at = None


def post_detail(request, post_id, post_slug=None):
    publish_due_posts()

    post = get_object_or_404(
        Post.objects.select_related('author', 'author__profile', 'category').prefetch_related(
            'comments__author__profile',
            'images',
            'tags',
            'quiz_options',
            'poll_options'
        ),
        id=post_id,
        status='published'
    )

    if request.method == "GET":
        expected_slug = _bp_post_public_slug(post)
        if post_slug != expected_slug:
            return redirect(_bp_post_public_url(post))

    session_key = f'viewed_post_{post.id}'

    if request.user != post.author and not request.session.get(session_key):
        post.views += 1
        post.save(update_fields=['views'])
        request.session[session_key] = True

    comments = post.comments.all().order_by('created_at', 'id')
    blog_preferences = apply_blog_preferences_to_profile(post.author.profile, post.author)
    allow_anonymous_comments = get_allow_anonymous_comments(post.author)
    post.allow_anonymous_comments = allow_anonymous_comments

    if request.method == 'POST':
        if not blog_preferences.get('allow_comments', True) or not post.allow_comments:
            messages.error(request, 'Komentari su isključeni za ovaj post.')
            return redirect(_bp_post_public_url(post))

        if request.user.is_authenticated and is_user_restricted(post.author, request.user):
            messages.error(request, 'Autor te je ograničio pa ne možeš komentirati.')
            return redirect(_bp_post_public_url(post))

        form = CommentForm(request.POST)

        if form.is_valid():
            wants_anonymous = form.cleaned_data.get('anonymous', False)
            if not request.user.is_authenticated:
                messages.error(request, 'Za komentiranje je potrebna registracija.')
                return redirect('login')

            if wants_anonymous and not allow_anonymous_comments:
                messages.error(request, 'Anonimno komentiranje nije dopušteno za ovaj blog.')
                return redirect(_bp_post_public_url(post))

            is_anonymous_comment = bool(wants_anonymous and allow_anonymous_comments)

            comment_content = (form.cleaned_data.get('content') or '').strip()
            allowed, error_message = check_comment_allowed(request, post, comment_content)

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
                return redirect(_bp_post_public_url(post))

            comment = form.save(commit=False)
            comment.post = post

            comment.author = request.user
            comment.is_anonymous = is_anonymous_comment
            comment.save()
            remember_comment_sent(request, post, comment_content)

            if request.user.is_authenticated and not is_anonymous_comment and request.user != post.author:
                Notification.objects.create(
                    recipient=post.author,
                    sender=request.user,
                    post=post,
                    comment=comment,
                    notification_type='comment'
                )

            return redirect(_bp_comment_public_url(comment))
    else:
        form = CommentForm()

    if (not request.user.is_authenticated or not allow_anonymous_comments) and 'anonymous' in form.fields:
        form.fields['anonymous'].widget = form.fields['anonymous'].hidden_widget()

    post.user_liked = request.user.is_authenticated and post.likes.filter(user=request.user).exists()
    enrich_posts_with_quiz_poll_data([post], request.user)

    today = timezone.localdate()
    local_publication_datetime = get_post_publication_datetime(post)
    base_year = local_publication_datetime.year
    base_month = local_publication_datetime.month

    try:
        calendar_year = int(request.GET.get('year')) if request.GET.get('year') else base_year
    except (TypeError, ValueError):
        calendar_year = base_year

    try:
        calendar_month = int(request.GET.get('month')) if request.GET.get('month') else base_month
    except (TypeError, ValueError):
        calendar_month = base_month

    if calendar_month < 1 or calendar_month > 12:
        calendar_year = base_year
        calendar_month = base_month

    current_day = today.day if calendar_year == today.year and calendar_month == today.month else None
    month_calendar, days_with_posts, day_single_post_map = build_calendar_for_user(post.author, calendar_year, calendar_month)
    archives = build_archives_for_user(post.author)

    prev_month_url, next_month_url = build_month_navigation_urls(
        _bp_post_public_url(post),
        calendar_year,
        calendar_month,
    )

    live_analytics = build_live_analytics_context(post.author)
    analytics_tracking = build_tracking_context(post.author, blog_preferences, page_label='post')

    context = {
        'blog': post.author,
        'page_obj': [post],
        'comments': comments,
        'form': form,
        'is_detail': True,
        'month_calendar': month_calendar,
        'current_day': current_day,
        'current_month_num': calendar_month,
        'current_month_hr': MONTHS_HR.get(calendar_month, ''),
        'current_year': calendar_year,
        'prev_month_url': prev_month_url,
        'next_month_url': next_month_url,
        'days_with_posts': days_with_posts,
        'day_single_post_map': day_single_post_map,
        'archives': archives,
        'left_boxes': UserBox.objects.filter(user=post.author, position='left').order_by('order'),
        'right_boxes': UserBox.objects.filter(user=post.author, position='right').order_by('order'),
        'is_following': request.user.is_authenticated and post.author.followers.filter(follower=request.user).exists(),
        'is_restricted': is_user_restricted(post.author, request.user),
        'followers_count': post.author.followers.count(),
        'following_count': post.author.following.count(),
        'archive_base_url': reverse('user_blog', args=[post.author.username]),
        'has_author_content': has_public_author_content(post.author.profile),
        'author_profile_items': build_author_profile_items(post.author.profile),
        'author_page_url': reverse('author_detail', args=[post.author.username]),
        'allow_anonymous_comments': allow_anonymous_comments,
        'anonymous_comment_username': ANONYMOUS_COMMENT_USERNAME,
        'blog_preferences': blog_preferences,
        'live_analytics': live_analytics,
        'analytics_tracking': analytics_tracking,
    }

    return render(request, resolve_design_template_name(post.author.profile.template), context)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.allow_comments = form.cleaned_data.get('allow_comments', True)

            submit_action = 'draft' if 'save_draft' in request.POST else 'publish'
            publish_at = form.cleaned_data.get('publish_at') if submit_action == 'publish' else None
            _apply_submit_action_to_post(post, submit_action, publish_at)

            if submit_action == 'publish' and not post.category:
                form.add_error('category', 'Odaberi kategoriju prije objave posta.')
            else:
                post.save()
                apply_tags_to_post(post, form.cleaned_data.get('tags_list', []))
                return redirect('home')
    else:
        form = PostForm(initial={'allow_comments': True})
    return render(request, 'blog/create_post.html', {'form': form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(
        Post.objects.prefetch_related('images', 'tags'),
        id=post_id,
        author=request.user
    )

    categories = Category.objects.all().order_by('group', 'name', 'id')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)

        if request.POST.get('delete_image') and post.image:
            post.image.delete(save=False)
            post.image = None
            post.save(update_fields=['image'])

        for image_id in request.POST.getlist('delete_post_image_ids'):
            post_image = post.images.filter(id=image_id).first()

            if post_image:
                post_image.image.delete(save=False)
                post_image.delete()

        if form.is_valid():
            post = form.save(commit=False)
            post.allow_comments = form.cleaned_data.get('allow_comments', True)

            submit_action = 'draft' if 'save_draft' in request.POST else 'publish'
            publish_at = form.cleaned_data.get('publish_at') if submit_action == 'publish' else None
            _apply_submit_action_to_post(post, submit_action, publish_at)

            if submit_action == 'publish' and not post.category:
                form.add_error('category', 'Odaberi kategoriju prije objave posta.')
            else:
                post.save()
                apply_tags_to_post(post, form.cleaned_data.get('tags_list', []))

                for upload in request.FILES.getlist('images'):
                    PostImage.objects.create(post=post, image=upload)

                if post.status == 'published':
                    return redirect(_bp_post_public_url(post))

                if post.status == 'scheduled':
                    return redirect('/blog/settings/?tab=postovi&post_filter=scheduled')

                return redirect('/blog/settings/?tab=postovi&post_filter=draft')
    else:
        form = PostForm(instance=post)

    return render(
        request,
        'blog/edit_post.html',
        {
            'form': form,
            'post': post,
            'categories': categories,
        }
    )

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post_title = post.title
        post_id_value = post.id
        post.delete()
        log_security_event(
            request,
            event_type='post_deleted',
            user=request.user,
            severity='warning',
            message='Korisnik je trajno izbrisao post.',
            metadata={'post_id': post_id_value, 'post_title': post_title},
        )
        return redirect('home')
    return render(request, 'blog/delete_post.html', {'post': post})
