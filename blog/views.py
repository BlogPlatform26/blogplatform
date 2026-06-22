from blog.view_handlers.analytics_views import *
from blog.view_handlers.auth_views import *
from blog.view_handlers.blog_views import *
from blog.view_handlers.interaction_views import *
from blog.view_handlers.notification_views import *
from blog.view_handlers.post_views import *
from blog.view_handlers.security_views import *
from blog.view_handlers.settings_views import *
from blog.view_handlers.user_views import *
from blog.view_handlers.post_export_views import *
from blog.view_handlers.admin_post_export_views import *
from blog.view_handlers.basic_pages_views import *

# BLOGPLATFORM ACCOUNT ACTION URL EXPORTS
# Ovo treba postojati jer blogplatform/urls.py koristi views.deactivate_account,
# views.request_delete_account i views.reactivate_account.

def deactivate_account(request, *args, **kwargs):
    from blog.view_handlers.settings_views import deactivate_account as _view
    return _view(request, *args, **kwargs)


def request_delete_account(request, *args, **kwargs):
    from blog.view_handlers.settings_views import request_delete_account as _view
    return _view(request, *args, **kwargs)


def reactivate_account(request, *args, **kwargs):
    from blog.view_handlers.auth_views import reactivate_account as _view
    return _view(request, *args, **kwargs)
