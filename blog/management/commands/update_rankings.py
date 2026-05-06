from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Count
from datetime import datetime, timedelta, time
import math

from blog.models import Post, FeaturedPost


def clamp(v, a, b):
    return max(a, min(b, v))


def compute_post_score(post, now):
    likes = getattr(post, "_likes_count", 0)
    comments = getattr(post, "_comments_count", 0)
    views = post.views or 0

    w_views = 2.0
    w_like = 8.0
    w_comment = 10.0

    base = (w_views * math.log1p(views)) + (w_like * likes) + (w_comment * comments)

    age_seconds = (now - post.created_at).total_seconds()
    age_hours = max(0.0, age_seconds / 3600.0)

    freshness = 1.20 - (age_hours / 240.0)
    freshness = clamp(freshness, 0.85, 1.20)

    return float(base * freshness)


def pick_best_post(period_start_dt, period_end_dt):
    now = timezone.now()

    qs = (Post.objects
          .filter(status="published",
                  created_at__gte=period_start_dt,
                  created_at__lt=period_end_dt)
          .annotate(_likes_count=Count("likes", distinct=True),
                    _comments_count=Count("comments", distinct=True)))

    best = None
    best_score = -1

    for p in qs:
        s = compute_post_score(p, now)
        if s > best_score:
            best_score = s
            best = p

    return best, best_score


class Command(BaseCommand):
    help = "Ažurira Post dana i Post tjedna (sprema u FeaturedPost)."

    def handle(self, *args, **options):
        tz = timezone.get_current_timezone()
        today = timezone.localdate()

        # POST DANA: jučer (00:00 - danas 00:00)
        day_start = datetime.combine(today - timedelta(days=1), time(0, 0))
        day_end = datetime.combine(today, time(0, 0))
        day_start = timezone.make_aware(day_start, tz)
        day_end = timezone.make_aware(day_end, tz)

        best_post, best_score = pick_best_post(day_start, day_end)

        if best_post:
            FeaturedPost.objects.update_or_create(
                kind="daily",
                period_start=day_start,
                defaults={
                    "period_end": day_end,
                    "post": best_post,
                    "score": best_score
                }
            )
            self.stdout.write(self.style.SUCCESS(
                f"Post dana ({today - timedelta(days=1)}): {best_post.id} score={best_score:.2f}"
            ))
        else:
            self.stdout.write("Post dana: nema postova u periodu.")

        # POST TJEDNA: prošli cijeli tjedan (pon -> pon)
        weekday = today.isoweekday()
        this_monday = today - timedelta(days=(weekday - 1))
        prev_monday = this_monday - timedelta(days=7)

        week_start = datetime.combine(prev_monday, time(0, 0))
        week_end = datetime.combine(this_monday, time(0, 0))
        week_start = timezone.make_aware(week_start, tz)
        week_end = timezone.make_aware(week_end, tz)

        best_week_post, best_week_score = pick_best_post(week_start, week_end)

        if best_week_post:
            FeaturedPost.objects.update_or_create(
                kind="weekly",
                period_start=week_start,
                defaults={
                    "period_end": week_end,
                    "post": best_week_post,
                    "score": best_week_score
                }
            )
            self.stdout.write(self.style.SUCCESS(
                f"Post tjedna ({prev_monday} - {this_monday}): {best_week_post.id} score={best_week_score:.2f}"
            ))
        else:
            self.stdout.write("Post tjedna: nema postova u periodu.")