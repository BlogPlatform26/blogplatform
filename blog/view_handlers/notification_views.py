from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from blog.models import Notification


@login_required
def notifications(request):
    notifications_qs = request.user.notifications.all().order_by('-created_at')
    return render(request, 'blog/notifications.html', {'notifications': notifications_qs})


@login_required
@require_POST
def mark_all_notifications_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect(request.META.get('HTTP_REFERER', 'notifications'))


@login_required
@require_POST
def notification_redirect(request, notification_id):
    notification = get_object_or_404(
        Notification,
        id=notification_id,
        recipient=request.user,
    )

    if not notification.is_read:
        notification.is_read = True
        notification.save(update_fields=['is_read'])

    if notification.notification_type == 'follow' and notification.sender_id:
        return redirect('user_blog', username=notification.sender.username)

    if notification.notification_type == 'comment' and notification.post_id:
        if notification.comment_id:
            return redirect(
                f"{reverse('post_detail', args=[notification.post.id])}#comment-{notification.comment.id}"
            )
        return redirect('post_detail', post_id=notification.post.id)

    if notification.notification_type == 'like' and notification.post_id:
        return redirect('post_detail', post_id=notification.post.id)

    return redirect('home')
