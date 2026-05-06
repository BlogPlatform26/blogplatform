from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from datetime import timedelta
import math
from .forms import BugReportForm
from .models import SiteMessage
from .models import Notification, Comment, Post, FeaturedPost
from .services import (
    DEFAULT_BLOG_PREFERENCES,
    annotate_publication_datetime,
    build_design_customization_payload,
    normalize_design_customizations,
    publish_due_posts,
)


def clamp(v, a, b):
    return max(a, min(b, v))


def compute_user_score(total_views, total_likes, total_comments):
    total_views = total_views or 0
    total_likes = total_likes or 0
    total_comments = total_comments or 0

    w_views = 1.6
    w_like = 8.0
    w_comment = 10.0

    return float(w_views * math.log1p(total_views) + w_like * total_likes + w_comment * total_comments)


def get_top_bloggers(days=30):
    since = timezone.now() - timedelta(days=days)

    rows = (annotate_publication_datetime(Post.objects.filter(status="published"))
            .filter(publication_datetime_db__gte=since, publication_datetime_db__lte=timezone.now())
            .values("author")
            .annotate(
                total_views=Sum("views"),
                total_likes=Count("likes", distinct=True),
                total_comments=Count("comments", distinct=True),
                posts_count=Count("id", distinct=True)
            ))

    data = []
    for r in rows:
        data.append({
            "user_id": r["author"],
            "score": compute_user_score(r["total_views"], r["total_likes"], r["total_comments"]),
            "posts_count": r["posts_count"],
        })

    if not data:
        return []

    total_bloggers = len(data)
    k = math.ceil(total_bloggers * 0.05)
    k = int(clamp(k, 5, 10))

    data.sort(key=lambda x: x["score"], reverse=True)
    top = data[:k]

    users_map = {u.id: u for u in User.objects.select_related("profile").filter(id__in=[t["user_id"] for t in top])}

    result = []
    for t in top:
        u = users_map.get(t["user_id"])
        if not u:
            continue
        result.append({
            "user": u,
            "score": t["score"],
            "posts_count": t["posts_count"],
        })

    return result


def get_default_blog_preferences_context():
    prefs = DEFAULT_BLOG_PREFERENCES.copy()
    prefs["design_customizations"] = normalize_design_customizations(
        prefs.get("design_customizations")
    )
    prefs["active_design_customization"] = build_design_customization_payload(
        prefs["design_customizations"].get("default", {})
    )
    prefs.setdefault("cursor_style", "default")
    prefs.setdefault("cursor_effect", "none")
    prefs.setdefault("cursor_stylesheet_url", "")
    prefs.setdefault("cursor_css", "auto")
    prefs.setdefault("cursor_pointer_css", "pointer")
    prefs.setdefault("ambient_music_enabled", False)
    prefs.setdefault("ambient_music_track_data", None)
    prefs.setdefault("ambient_music_volume", 18)
    return prefs


def notifications_data(request):
    publish_due_posts()
    # ✅ Notifikacije (navbar)
    if request.user.is_authenticated:
        unread_notifications_count = request.user.notifications.filter(is_read=False).count()
        latest_notifications = request.user.notifications.select_related(
            "sender", "post", "comment"
        ).order_by("-created_at")[:10]
    else:
        unread_notifications_count = 0
        latest_notifications = []

    # ✅ Najnoviji komentari (sidebar)
    latest_comments = (Comment.objects
                       .select_related("author", "post")
                       .order_by("-created_at")[:5])

    # ✅ Post dana / Post tjedna (iz baze)
    fp_day = (FeaturedPost.objects
              .select_related("post", "post__author", "post__author__profile")
              .filter(kind="daily")
              .order_by("-period_start")
              .first())

    fp_week = (FeaturedPost.objects
               .select_related("post", "post__author", "post__author__profile")
               .filter(kind="weekly")
               .order_by("-period_start")
               .first())

    post_of_day = fp_day.post if fp_day else None
    post_of_week = fp_week.post if fp_week else None

    # ✅ Top blogeri
    top_bloggers = get_top_bloggers(days=30)
    bug_form = BugReportForm()
    site_msg = SiteMessage.objects.first()

    return {
        "unread_notifications_count": unread_notifications_count,
        "latest_notifications": latest_notifications,
        "latest_comments": latest_comments,
        "post_of_day": post_of_day,
        "post_of_week": post_of_week,
        "top_bloggers": top_bloggers,
        "bug_form": bug_form,
        "site_msg": site_msg,
        "blog_preferences": get_default_blog_preferences_context(),
    }
