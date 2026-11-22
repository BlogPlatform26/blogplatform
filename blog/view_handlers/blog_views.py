from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Prefetch, Q
from django.shortcuts import render
from django.utils import timezone

from blog.models import Category, Follow, Like, Post, PostImage, Tag
from blog.services import annotate_publication_datetime, apply_blog_preferences_to_posts, get_active_category_name, get_home_featured_entries, get_home_featured_posts, get_special_day_cards, publish_due_home_featured_posts, publish_due_posts



def _mark_liked_posts(posts, user):
    post_list = list(posts or [])

    if not post_list:
        return

    if not getattr(user, "is_authenticated", False):
        for post in post_list:
            post.user_liked = False
        return

    liked_ids = set(
        Like.objects.filter(
            user=user,
            post_id__in=[post.id for post in post_list]
        ).values_list("post_id", flat=True)
    )

    for post in post_list:
        post.user_liked = post.id in liked_ids


def home(request):
    publish_due_posts()
    now = timezone.now()
    publish_due_home_featured_posts(now=now)
    filter_type = (request.GET.get('filter') or '').strip()
    if filter_type not in ('featured', 'following', 'all'):
        filter_type = 'featured'

    blocked_ids = []
    if request.user.is_authenticated:
        blocked_ids = list(request.user.blocking.values_list('blocked_id', flat=True)) + list(request.user.blocked_by.values_list('blocker_id', flat=True))

    base_post_list = annotate_publication_datetime(Post.objects.filter(status='published')).filter(publication_datetime_db__lte=now)

    if blocked_ids:
        base_post_list = base_post_list.exclude(author_id__in=blocked_ids)

    category_slug = request.GET.get('category')
    tag_name = request.GET.get('tag')

    if category_slug:
        base_post_list = base_post_list.filter(category__slug=category_slug)
    if tag_name:
        base_post_list = base_post_list.filter(tags__name=tag_name)

    ordered_post_list = (
        base_post_list.distinct()
        .select_related('author', 'author__profile', 'category')
        .prefetch_related(Prefetch('images', queryset=PostImage.objects.order_by('pk')), 'tags')
        .order_by('-publication_datetime_db', '-created_at')
    )

    per_page = int(request.session.get('posts_per_page', 5) or 5)
    if per_page not in (5, 10, 15, 20):
        per_page = 5

    featured_primary_posts = []
    featured_secondary_posts = []
    featured_page = None

    if filter_type == 'featured':
        entries = get_home_featured_entries(base_post_list, now=now)
        featured_per_page = 6
        featured_page = Paginator(entries, featured_per_page).get_page(request.GET.get('page'))

        primary_start = (featured_page.number - 1) * featured_per_page
        displayed_posts = get_home_featured_posts(
            entries[primary_start:primary_start + 2 * featured_per_page]
        )
        apply_blog_preferences_to_posts(displayed_posts)
        _mark_liked_posts(displayed_posts, request.user)

        featured_primary_posts = displayed_posts[:featured_per_page]
        featured_secondary_posts = displayed_posts[featured_per_page:]
        featured_page.object_list = featured_primary_posts
        posts = featured_page
    else:
        if request.user.is_authenticated and filter_type == 'following':
            following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
            ordered_post_list = ordered_post_list.filter(author__in=following_users)

        posts = Paginator(ordered_post_list, per_page).get_page(request.GET.get('page'))
        apply_blog_preferences_to_posts(posts)
        _mark_liked_posts(posts, request.user)

    following_posts = []
    if request.user.is_authenticated:
        following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
        following_posts = annotate_publication_datetime(Post.objects.filter(author__in=following_users, status='published')).filter(publication_datetime_db__lte=now).order_by('-publication_datetime_db', '-created_at')[:5]

    return render(request, 'blog/home.html', {
        'posts': posts,
        'featured_page': featured_page,
        'featured_primary_posts': featured_primary_posts,
        'featured_secondary_posts': featured_secondary_posts,
        'following_posts': following_posts,
        'active_category': category_slug,
        'active_tag': tag_name,
        'filter_type': filter_type,
        'active_category_name': get_active_category_name(category_slug),
        'special_day_cards': get_special_day_cards(),
    })


def search(request):
    publish_due_posts()
    q = (request.GET.get('q') or '').strip()
    scope = (request.GET.get('scope') or 'all').strip()

    posts = Post.objects.none()
    users = User.objects.none()
    tags = Tag.objects.none()
    posts_total = users_total = tags_total = 0

    if q:
        posts_qs = (
            annotate_publication_datetime(Post.objects.filter(status='published')).filter(publication_datetime_db__lte=timezone.now())
            .filter(
                Q(title__icontains=q)
                | Q(content__icontains=q)
                | Q(author__username__icontains=q)
                | Q(category__name__icontains=q)
                | Q(tags__name__icontains=q)
            )
            .distinct()
            .order_by('-publication_datetime_db', '-created_at')
        )
        posts_total = posts_qs.count()
        if scope in ('all', 'posts'):
            posts = Paginator(posts_qs, 5).get_page(request.GET.get('page'))
            apply_blog_preferences_to_posts(posts)
            _mark_liked_posts(posts, request.user)

        users_qs = (
            User.objects.select_related('profile')
            .filter(Q(username__icontains=q) | Q(profile__blog_name__icontains=q))
            .distinct()
            .order_by('username')
        )
        users_total = users_qs.count()
        if scope in ('all', 'users'):
            users = users_qs[:30]

        tags_qs = Tag.objects.filter(name__icontains=q)
        tags_total = tags_qs.count()
        if scope in ('all', 'tags'):
            tags = tags_qs.annotate(
                published_posts=Count('posts', filter=Q(posts__status='published'), distinct=True)
            ).order_by('-published_posts', 'name')[:40]

    return render(request, 'blog/search.html', {
        'q': q,
        'scope': scope,
        'posts': posts,
        'users_found': users,
        'tags_found': tags,
        'posts_total': posts_total,
        'users_total': users_total,
        'tags_total': tags_total,
    })
