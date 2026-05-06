from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from blog.forms import AuthorQuestionForm
from blog.models import AuthorQuestion, Follow, Like, UserBlock, UserRestriction, UserBox
from blog.services import (
    apply_blog_preferences_to_profile,
    are_users_blocked,
    build_archives_for_user,
    build_author_profile_items,
    build_author_profile_sections,
    build_calendar_for_user,
    build_month_navigation_urls,
    get_blog_page_response,
    get_private_author_questions_for_viewer,
    get_public_author_questions,
    has_public_author_content,
    is_user_restricted,
    resolve_design_template_name,
)
from blog.constants import MONTHS_HR


@login_required
def profile(request):
    return get_blog_page_response(
        request,
        request.user,
        resolve_design_template_name(request.user.profile.template),
        allow_follow=False,
        archive_base_url='/profile/',
    )


def user_blog(request, username):
    blog_user = get_object_or_404(User.objects.select_related('profile'), username=username)
    if request.user.is_authenticated and are_users_blocked(request.user, blog_user):
        messages.error(request, 'Ovaj blog nije dostupan zbog blokiranja.')
        return redirect('home')
    return get_blog_page_response(
        request,
        blog_user,
        resolve_design_template_name(blog_user.profile.template),
        allow_follow=True,
    )


def author_detail(request, username):
    blog_user = get_object_or_404(User.objects.select_related('profile'), username=username)

    if request.user.is_authenticated and are_users_blocked(request.user, blog_user):
        messages.error(request, 'Ovaj blog nije dostupan zbog blokiranja.')
        return redirect('home')

    if not has_public_author_content(blog_user.profile):
        messages.info(request, 'Autor još nije ispunio dio Upoznaj autora.')
        return redirect('user_blog', username=blog_user.username)

    from django.utils import timezone
    today = timezone.localdate()

    year_param = request.GET.get('year')
    month_param = request.GET.get('month')

    try:
        display_year = int(year_param) if year_param else today.year
    except (TypeError, ValueError):
        display_year = today.year

    try:
        display_month = int(month_param) if month_param else today.month
    except (TypeError, ValueError):
        display_month = today.month

    if display_month < 1 or display_month > 12:
        display_month = today.month
        display_year = today.year

    month_calendar, days_with_posts, day_single_post_map = build_calendar_for_user(
        blog_user,
        display_year,
        display_month,
    )
    archives = build_archives_for_user(blog_user)
    prev_month_url, next_month_url = build_month_navigation_urls(
        request.path,
        display_year,
        display_month,
    )

    blog_preferences = apply_blog_preferences_to_profile(blog_user.profile, blog_user)

    question_form = None
    can_ask_questions = False
    if request.user.is_authenticated and request.user != blog_user and not is_user_restricted(blog_user, request.user):
        can_ask_questions = blog_user.profile.allow_author_questions
        question_form = AuthorQuestionForm()

    public_author_questions = get_public_author_questions(blog_user)
    viewer_private_author_questions = get_private_author_questions_for_viewer(blog_user, request.user)

    context = {
        'blog': blog_user,
        'left_boxes': UserBox.objects.filter(user=blog_user, position='left').order_by('order'),
        'right_boxes': UserBox.objects.filter(user=blog_user, position='right').order_by('order'),
        'month_calendar': month_calendar,
        'current_day': today.day if display_year == today.year and display_month == today.month else None,
        'current_month_num': display_month,
        'current_month_hr': MONTHS_HR.get(display_month, ''),
        'current_year': display_year,
        'days_with_posts': days_with_posts,
        'day_single_post_map': day_single_post_map,
        'archives': archives,
        'archive_base_url': f'/blog/{blog_user.username}/',
        'prev_month_url': prev_month_url,
        'next_month_url': next_month_url,
        'is_following': request.user.is_authenticated and Follow.objects.filter(follower=request.user, following=blog_user).exists(),
        'is_restricted': is_user_restricted(blog_user, request.user),
        'followers_count': Follow.objects.filter(following=blog_user).count(),
        'following_count': Follow.objects.filter(follower=blog_user).count(),
        'blog_preferences': blog_preferences,
        'author_profile_items': build_author_profile_items(blog_user.profile),
        'author_profile_sections': build_author_profile_sections(blog_user.profile),
        'author_bio': blog_user.profile.author_bio,
        'has_author_content': True,
        'author_page_url': request.path,
        'public_author_questions': public_author_questions,
        'viewer_private_author_questions': viewer_private_author_questions,
        'question_form': question_form,
        'can_ask_author_question': can_ask_questions,
    }
    return render(request, 'blog/author_detail.html', context)


@login_required
@require_POST
def submit_author_question(request, username):
    blog_user = get_object_or_404(User.objects.select_related('profile'), username=username)

    if request.user == blog_user:
        messages.info(request, 'Ne možeš sam sebi postavljati pitanja.')
        return redirect('author_detail', username=blog_user.username)

    if are_users_blocked(request.user, blog_user):
        messages.error(request, 'Ne možeš postaviti pitanje ovom autoru.')
        return redirect('home')

    if is_user_restricted(blog_user, request.user):
        messages.error(request, 'Autor te je ograničio pa mu ne možeš postaviti pitanje.')
        return redirect('author_detail', username=blog_user.username)

    if not blog_user.profile.allow_author_questions:
        messages.info(request, 'Autor trenutno ne prima pitanja.')
        return redirect('author_detail', username=blog_user.username)

    form = AuthorQuestionForm(request.POST)
    if form.is_valid():
        AuthorQuestion.objects.create(
            author=blog_user,
            sender=request.user,
            question=form.cleaned_data['question'],
        )
        messages.success(request, 'Pitanje je poslano autoru.')
    else:
        messages.error(request, form.errors.get('question', ['Pitanje nije poslano.'])[0])

    return redirect('author_detail', username=blog_user.username)


def blog_list(request):
    return render(request, 'blog/blog_list.html', {'users': User.objects.all()})


@login_required
@require_POST
def follow_toggle(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if request.user == user_to_follow:
        return redirect('user_blog', username=username)
    if are_users_blocked(request.user, user_to_follow):
        messages.error(request, 'Ne možeš pratiti ovog korisnika (blokiranje).')
        return redirect('user_blog', username=username)
    if is_user_restricted(user_to_follow, request.user):
        messages.error(request, 'Ovaj korisnik te je ograničio pa ga ne možeš pratiti.')
        return redirect('user_blog', username=username)

    follow, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    if created:
        from blog.models import Notification
        Notification.objects.create(recipient=user_to_follow, sender=request.user, notification_type='follow')
    else:
        follow.delete()
    return redirect('user_blog', username=username)


@login_required
@require_POST
def block_user(request, username):
    target = get_object_or_404(User, username=username)
    if target == request.user:
        return redirect('user_blog', username=username)

    UserBlock.objects.get_or_create(blocker=request.user, blocked=target)
    UserRestriction.objects.filter(owner=request.user, restricted=target).delete()
    Follow.objects.filter(follower=request.user, following=target).delete()
    Follow.objects.filter(follower=target, following=request.user).delete()
    Like.objects.filter(user=target, post__author=request.user).delete()
    messages.success(request, f'Blokirao si korisnika {target.username}.')
    return redirect('user_blog', username=username)


@login_required
@require_POST
def restrict_user(request, username):
    target = get_object_or_404(User, username=username)
    if target == request.user:
        return redirect('user_blog', username=username)

    restriction, created = UserRestriction.objects.get_or_create(owner=request.user, restricted=target)
    Follow.objects.filter(follower=target, following=request.user).delete()
    Like.objects.filter(user=target, post__author=request.user).delete()

    if created:
        messages.success(request, f'Ograničio si korisnika {target.username}.')
    else:
        messages.info(request, f'Korisnik {target.username} je već ograničen.')
    return redirect('user_blog', username=username)


@login_required
@require_POST
def unfollow_user(request, username):
    target = get_object_or_404(User, username=username)
    if target == request.user:
        return redirect('user_blog', username=username)

    deleted_count, _ = Follow.objects.filter(follower=request.user, following=target).delete()
    if deleted_count:
        messages.success(request, f'Više ne pratiš korisnika {target.username}.')
    else:
        messages.info(request, f'Ne pratiš korisnika {target.username}.')
    return redirect('user_blog', username=username)
