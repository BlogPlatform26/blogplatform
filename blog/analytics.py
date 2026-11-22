from collections import Counter
from datetime import timedelta

from django.utils import timezone

from .models import BlogVisitor


ACTIVE_WINDOW_MINUTES = 5
RECENT_WINDOW_MINUTES = 15
MAP_LOOKBACK_DAYS = 30


PAGE_LABELS = {
    'blog': 'Blog naslovnica',
    'post': 'Detalj posta',
}


def analytics_enabled(preferences):
    preferences = preferences or {}
    return bool(
        preferences.get('analytics_live_counter_enabled')
        or preferences.get('analytics_map_enabled')
        or preferences.get('analytics_active_pages_enabled')
    )


def classify_device_type(user_agent):
    value = (user_agent or '').lower()
    if not value:
        return 'Nepoznato'
    if any(word in value for word in ('bot', 'spider', 'crawl', 'slurp', 'preview')):
        return 'Bot'
    if any(word in value for word in ('ipad', 'tablet')):
        return 'Tablet'
    if any(word in value for word in ('iphone', 'android', 'mobile', 'opera mini', 'windows phone')):
        return 'Mobitel'
    return 'Računalo'


def _normalize_coordinate(value, minimum, maximum):
    if value in (None, ''):
        return None
    try:
        number = round(float(value), 1)
    except (TypeError, ValueError):
        return None
    if number < minimum or number > maximum:
        return None
    return number


def _normalize_text(value, limit):
    value = str(value or '').strip()
    if not value:
        return ''
    return value[:limit]


def _compose_location_label(city='', country='', timezone_name=''):
    parts = []
    if city:
        parts.append(city)
    if country and country not in parts:
        parts.append(country)
    if not parts and timezone_name:
        parts.append(timezone_name)
    return ', '.join(parts) if parts else 'Približna lokacija posjeta'


def track_blog_visit(
    owner,
    visitor_token,
    page_label='',
    path='',
    user_agent='',
    language='',
    timezone_name='',
    latitude=None,
    longitude=None,
    country='',
    country_code='',
    city='',
):
    if not owner or not visitor_token:
        return None

    token = str(visitor_token).strip()[:64]
    if len(token) < 8:
        return None

    lat = _normalize_coordinate(latitude, -90, 90)
    lon = _normalize_coordinate(longitude, -180, 180)
    country = _normalize_text(country, 80)
    country_code = _normalize_text(country_code, 8).upper()
    city = _normalize_text(city, 80)

    visit, created = BlogVisitor.objects.get_or_create(
        blog_owner=owner,
        visitor_token=token,
        defaults={
            'page_label': str(page_label or 'blog')[:50],
            'path': str(path or '')[:255],
            'device_type': classify_device_type(user_agent),
            'user_agent': str(user_agent or '')[:255],
            'browser_language': str(language or '')[:32],
            'timezone_name': str(timezone_name or '')[:64],
            'latitude': lat,
            'longitude': lon,
            'country': country,
            'country_code': country_code,
            'city': city,
            'hit_count': 1,
        },
    )

    if created:
        return visit

    visit.page_label = str(page_label or visit.page_label or 'blog')[:50]
    visit.path = str(path or visit.path or '')[:255]
    visit.device_type = classify_device_type(user_agent) or visit.device_type
    visit.user_agent = str(user_agent or visit.user_agent or '')[:255]
    visit.browser_language = str(language or visit.browser_language or '')[:32]
    visit.timezone_name = str(timezone_name or visit.timezone_name or '')[:64]
    if lat is not None and lon is not None:
        visit.latitude = lat
        visit.longitude = lon
    if country:
        visit.country = country
    if country_code:
        visit.country_code = country_code
    if city:
        visit.city = city
    visit.hit_count = (visit.hit_count or 0) + 1
    visit.save()
    return visit


def _aggregate_map_points(queryset, limit=36):
    grouped = {}

    for visit in queryset:
        if visit.latitude is None or visit.longitude is None:
            continue

        key = (float(visit.latitude), float(visit.longitude))
        item = grouped.setdefault(
            key,
            {
                'latitude': float(visit.latitude),
                'longitude': float(visit.longitude),
                'count': 0,
                'labels': [],
            },
        )
        item['count'] += 1
        location_label = _compose_location_label(visit.city, visit.country, visit.timezone_name)
        if location_label not in item['labels']:
            item['labels'].append(location_label)

    points = []
    for item in grouped.values():
        points.append(
            {
                'latitude': item['latitude'],
                'longitude': item['longitude'],
                'count': item['count'],
                'size': min(18, 7 + (item['count'] * 2)),
                'label': ' • '.join(item['labels'][:2]) or 'Približna lokacija posjeta',
            }
        )

    points.sort(key=lambda item: (-item['count'], item['latitude'], item['longitude']))
    return points[:limit]


def _build_country_breakdown(queryset, total_count, limit=10):
    counter = Counter()
    for visit in queryset:
        country_name = (visit.country or '').strip() or 'Nepoznato'
        counter[country_name] += 1

    items = []
    for country_name, count in counter.most_common(limit):
        percent = round((count / total_count) * 100, 1) if total_count else 0
        items.append({
            'country': country_name,
            'count': count,
            'percent': percent,
        })
    return items


def _build_location_breakdown(queryset, limit=12):
    counter = Counter()
    label_parts = {}

    for visit in queryset:
        country_name = (visit.country or '').strip()
        city_name = (visit.city or '').strip()
        key = (city_name, country_name)
        counter[key] += 1
        label_parts[key] = {
            'city': city_name,
            'country': country_name,
        }

    items = []
    for (city_name, country_name), count in counter.most_common(limit):
        if city_name and country_name:
            label = f'{city_name}, {country_name}'
        elif country_name:
            label = country_name
        elif city_name:
            label = city_name
        else:
            label = 'Nepoznata lokacija'

        items.append({
            'label': label,
            'city': city_name or 'Nepoznato',
            'country': country_name or 'Nepoznato',
            'count': count,
        })

    return items


def build_live_analytics_context(owner):
    now = timezone.now()
    today = timezone.localdate()

    base_qs = BlogVisitor.objects.filter(blog_owner=owner).exclude(device_type='Bot')
    active_now_qs = base_qs.filter(last_seen__gte=now - timedelta(minutes=ACTIVE_WINDOW_MINUTES))
    recent_qs = base_qs.filter(last_seen__gte=now - timedelta(minutes=RECENT_WINDOW_MINUTES))
    month_qs = base_qs.filter(last_seen__gte=now - timedelta(days=MAP_LOOKBACK_DAYS))
    today_qs = base_qs.filter(last_seen__date=today)

    month_visits = list(month_qs)

    page_counter = Counter(
        PAGE_LABELS.get(label, 'Druga stranica')
        for label in active_now_qs.values_list('page_label', flat=True)
    )
    device_counter = Counter(active_now_qs.values_list('device_type', flat=True))
    if not device_counter:
        device_counter = Counter(month_qs.values_list('device_type', flat=True))

    page_breakdown = [
        {'label': label, 'count': count}
        for label, count in page_counter.most_common(4)
    ]
    device_breakdown = [
        {'label': label or 'Nepoznato', 'count': count}
        for label, count in device_counter.most_common(4)
        if count
    ]

    latest_seen = base_qs.order_by('-last_seen').values_list('last_seen', flat=True).first()
    map_points = _aggregate_map_points(month_visits)
    month_unique = len(month_visits)
    country_breakdown = _build_country_breakdown(month_visits, month_unique)
    location_breakdown = _build_location_breakdown(month_visits)

    return {
        'active_now': active_now_qs.count(),
        'active_recent': recent_qs.count(),
        'today_unique': today_qs.count(),
        'month_unique': month_unique,
        'repeat_visitors': month_qs.filter(hit_count__gt=1).count(),
        'page_breakdown': page_breakdown,
        'device_breakdown': device_breakdown,
        'map_points': map_points,
        'has_map_points': bool(map_points),
        'country_breakdown': country_breakdown,
        'location_breakdown': location_breakdown,
        'has_location_breakdown': bool(country_breakdown or location_breakdown),
        'latest_seen': latest_seen,
    }


def build_tracking_context(owner, preferences, page_label='blog'):
    if not analytics_enabled(preferences):
        return None

    return {
        'owner_username': owner.username,
        'page_label': page_label,
        'geo_enabled': bool(preferences.get('analytics_geo_enabled', False)),
    }
