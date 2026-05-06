from blog.view_handlers.analytics_views import *
from blog.view_handlers.auth_views import *
from blog.view_handlers.blog_views import *
from blog.view_handlers.interaction_views import *
from blog.view_handlers.post_views import *
from blog.view_handlers.settings_views import *
from blog.view_handlers.user_views import *


@login_required
def mark_all_notifications_read(request):
    if request.method == "POST":
        request.user.notifications.filter(is_read=False).update(is_read=True)

    return redirect(request.META.get("HTTP_REFERER", "home"))

