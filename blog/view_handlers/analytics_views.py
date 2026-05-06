import json

from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_GET, require_POST

from blog.analytics import build_live_analytics_context, track_blog_visit


def _summary_payload(owner):
    summary = build_live_analytics_context(owner)
    return {
        'active_now': summary['active_now'],
        'active_recent': summary['active_recent'],
        'today_unique': summary['today_unique'],
        'month_unique': summary['month_unique'],
        'repeat_visitors': summary['repeat_visitors'],
        'page_breakdown': summary['page_breakdown'],
        'device_breakdown': summary['device_breakdown'],
        'map_points': summary['map_points'],
        'has_map_points': summary['has_map_points'],
        'country_breakdown': summary['country_breakdown'],
        'location_breakdown': summary['location_breakdown'],
        'has_location_breakdown': summary['has_location_breakdown'],
        'latest_seen': summary['latest_seen'].isoformat() if summary['latest_seen'] else None,
    }


@require_POST
def analytics_ping(request):
    try:
        payload = json.loads(request.body.decode('utf-8') or '{}')
    except (TypeError, ValueError, json.JSONDecodeError):
        return HttpResponseBadRequest('Neispravan JSON.')

    owner_username = (payload.get('owner_username') or '').strip()
    visitor_token = payload.get('visitor_token')
    if not owner_username or not visitor_token:
        return HttpResponseBadRequest('Nedostaju podaci za analitiku.')

    owner = User.objects.filter(username=owner_username).first()
    if not owner:
        return JsonResponse({'ok': False, 'message': 'Blog nije pronađen.'}, status=404)

    if request.user.is_authenticated and request.user == owner:
        return JsonResponse({'ok': True, 'ignored': True, 'summary': _summary_payload(owner)})

    track_blog_visit(
        owner=owner,
        visitor_token=visitor_token,
        page_label=payload.get('page_label'),
        path=payload.get('path'),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        language=payload.get('language'),
        timezone_name=payload.get('timezone_name'),
        latitude=payload.get('latitude'),
        longitude=payload.get('longitude'),
        country=payload.get('country'),
        country_code=payload.get('country_code'),
        city=payload.get('city'),
    )

    return JsonResponse({'ok': True, 'summary': _summary_payload(owner)})


@require_GET
def blog_analytics_summary(request, username):
    owner = User.objects.filter(username=username).first()
    if not owner:
        return JsonResponse({'ok': False, 'message': 'Blog nije pronađen.'}, status=404)
    return JsonResponse({'ok': True, 'summary': _summary_payload(owner)})
