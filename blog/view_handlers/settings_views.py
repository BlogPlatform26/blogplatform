import base64
import json
import os
import uuid
from collections import defaultdict
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.db.models import Count, Q, Sum
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.urls import reverse
from PIL import Image, UnidentifiedImageError

from blog.analytics import build_live_analytics_context
from blog.forms import AuthorProfileForm, PostForm, UserBoxForm
from blog.music_library import get_ambient_music_categories, get_ambient_music_track, get_ambient_music_tracks
from blog.models import (
    AuthorQuestion,
    Category,
    Comment,
    Follow,
    Like,
    PollOption,
    PollVote,
    Post,
    PostImage,
    Profile,
    QuizAnswer,
    QuizOption,
    SiteMessage,
    UserBlock,
    UserBox,
    UserRestriction,
)
from blog.services import (
    apply_blog_preferences_to_profile,
    apply_tags_to_post,
    annotate_publication_datetime,
    assign_home_image,
    get_allow_anonymous_comments,
    get_blog_preferences,
    get_blog_cursor_choices,
    get_blog_cursor_effect_choices,
    get_design_background_image_choices,
    get_soho_cover_image_choices,
    get_design_font_choices,
    get_design_gradient_direction_choices,
    get_design_pattern_choices,
    is_simple_design_template,
    normalize_design_customizations,
    build_design_customization_payload,
    publish_due_posts,
    set_allow_anonymous_comments,
    set_blog_preferences,
)
from blog.security import log_security_event


MAX_BLOG_BANNER_SIZE = 2 * 1024 * 1024
MAX_BLOG_BANNER_WIDTH = 2200
MAX_BLOG_BANNER_HEIGHT = 900
MAX_BOXES_PER_SIDE = 3
MAX_CUSTOM_CURSOR_SIZE = 512 * 1024
ALLOWED_CUSTOM_CURSOR_EXTENSIONS = {'.png', '.svg', '.webp', '.cur'}


DESIGN_TEMPLATE_META = {
    'default': {
        'label': 'Default',
        'description': 'Svijetli izgled',
        'preview_image': 'blog/images/design-previews/default.png',
    },
    'dark': {
        'label': 'Dark',
        'description': 'Tamni izgled',
        'preview_image': 'blog/images/design-previews/dark.png',
    },
    'classic': {
        'label': 'Classic',
        'description': 'Klasični izgled',
        'preview_image': 'blog/images/design-previews/classic.png',
    },
    'default_right': {
        'label': 'Default Plus',
        'description': 'Širi post i bočni stupci',
        'preview_image': 'blog/images/design-previews/default_right.png',
    },
    'dark_right': {
        'label': 'Dark Plus',
        'description': 'Širi post i bočni stupci',
        'preview_image': 'blog/images/design-previews/dark_right.png',
    },
    'classic_right': {
        'label': 'Classic Plus',
        'description': 'Širi post i bočni stupci',
        'preview_image': 'blog/images/design-previews/classic_right.png',
    },
    'simple_pattern': {
        'label': 'Simple Uzorak',
        'description': 'Jednostavan blog s uzorcima pozadine',
        'preview_image': 'blog/images/design-previews/simple_pattern.png',
    },
    'simple_image': {
        'label': 'Simple Slika',
        'description': 'Jednostavan blog sa slikom u pozadini',
        'preview_image': 'blog/images/design-previews/simple_image.png',
    },
    'simple_retro': {
        'label': 'Simple Retro',
        'description': 'Vintage simple raspored s uzorkom gore, ravnim postovima i čistim desnim sidebarom',
        'preview_image': 'blog/images/design-previews/simple_retro.png',
    },
    'soho': {
        'label': 'Studio',
        'description': 'Lijevi stupac, razmak i velika naslovna slika',
        'preview_image': 'blog/images/design-previews/soho.png',
    },
    'magazin': {
        'label': 'Magazin',
        'description': 'Puni lijevi stupac, velika slika od ruba do ruba i post koji prelazi preko slike',
        'preview_image': 'blog/images/design-previews/magazin.png',
    },
    'litica_noci': {
        'label': 'Litica u noći',
        'description': 'Gornja slika i crna pozadina',
        'preview_image': 'blog/images/design-previews/litica_noci.png',
    },
    'podvodna_tisina': {
        'label': 'Podvodna tišina',
        'description': 'Gornja slika i tamna morska pozadina',
        'preview_image': 'blog/images/design-previews/podvodna_tisina.png',
    },
    'vodopad_u_magli': {
        'label': 'Vodopad u magli',
        'description': 'Gornja slika i svijetla pozadina',
        'preview_image': 'blog/images/design-previews/vodopad_u_magli.png',
    },
    'planine_u_magli': {
        'label': 'Planine u magli',
        'description': 'Maglovite planine, stakleni boxevi i svijetla pozadina',
        'preview_image': 'blog/images/design-previews/planine_u_magli.jpg',
    },
    'nebeski_mir': {
        'label': 'Nebeski mir',
        'description': 'Nježna pozadina oblaka, golubica i svijetli stakleni boxevi',
        'preview_image': 'blog/images/design-previews/nebeski_mir.jpg',
    },
    'svemirski_horizont': {
        'label': 'Svemirski horizont',
        'description': 'Pogled na Zemlju iz svemira, bez boxa oko posta i s prozirnim okvirima sa strane',
        'preview_image': 'blog/images/design-previews/svemirski_horizont.jpg',
    },
    'zlatni_horizont': {
        'label': 'Zlatni horizont',
        'description': 'Mirni morski zalazak, gornja slika i prijelaz u crnu pozadinu',
        'preview_image': 'blog/images/design-previews/zlatni_horizont.jpg',
    },
    'iznad_oblaka': {
        'label': 'Iznad oblaka',
        'description': 'Nježna slika iznad oblaka i prijelaz u crnu pozadinu',
        'preview_image': 'blog/images/design-previews/iznad_oblaka.jpg',
    },
    'sumska_svjetlost': {
        'label': 'Šumska svjetlost',
        'description': 'Šumska slika gore i nježni prijelaz u svijetlo zelenu pozadinu',
        'preview_image': 'blog/images/design-previews/sumska_svjetlost.jpg',
    },
    'polarna_svjetlost': {
        'label': 'Polarna svjetlost',
        'description': 'Polarna svjetlost, ledeni pejzaž i prijelaz u plavkastu pozadinu',
        'preview_image': 'blog/images/design-previews/polarna_svjetlost.jpg',
    },
    'zlatno_polje': {
        'label': 'Zlatno polje',
        'description': 'Pšenično polje, zalazak i prijelaz u zlaćanu pozadinu',
        'preview_image': 'blog/images/design-previews/zlatno_polje.jpg',
    },
    'neonski_grad': {
        'label': 'Neonski grad',
        'description': 'Moderni noćni grad, neon odsjaj i tamni stakleni boxevi',
        'preview_image': 'blog/images/design-previews/neonski_grad.jpg',
    },
    'polje_lavande': {
        'label': 'Polje lavande',
        'description': 'Lavanda, toplo nebo i prozirni boxevi bez pozadine',
        'preview_image': 'blog/images/design-previews/polje_lavande.jpg',
    },
    'carobna_ljubicasta': {
        'label': 'Čarobni sumrak',
        'description': 'Tamniji čarobni pejzaž, ljubičasti tonovi i poluprozirni boxevi',
        'preview_image': 'blog/images/design-previews/carobna_ljubicasta.jpg',
    },
    'kraljevska_pozornica': {
        'label': 'Kraljevska pozornica',
        'description': 'Kazališna pozornica gore i mekani prijelaz u tamno bordo pozadinu',
        'preview_image': 'blog/images/design-previews/kraljevska_pozornica.jpg',
    },
    'nebeska_klasika': {
        'label': 'Nebeska klasika',
        'description': 'Klasični blog template sa svijetlim nebom, centralnim sadržajem i desnim sidebarom',
        'preview_image': 'blog/images/design-previews/nebeska_klasika.jpg',
    },
    'ponocna_elegancija': {
        'label': 'Ponoćna elegancija',
        'description': 'Tamni elegantni dizajn sa zvjezdanim nebom, šumom i profinjenim svijetlim boxevima',
        'preview_image': 'blog/images/design-previews/ponocna_elegancija.png',
    },
    'ruzicasti_vrt': {
        'label': 'Ružičasti vrt',
        'description': 'Romantični dizajn s ružama, poluprozirnim boxevima i blagim blur efektom pozadine',
        'preview_image': 'blog/images/design-previews/ruzicasti_vrt.jpg',
    },
    'stara_aleja': {
        'label': 'Stara aleja',
        'description': 'Vintage tematski dizajn sa starinskom ulicom, toplim tonovima i elegantnim svijetlim boxevima',
        'preview_image': 'blog/images/design-previews/stara_aleja.jpg',
    },
    'staza_prema_vrhovima': {
        'label': 'Staza prema vrhovima',
        'description': 'Putopisni dizajn s planinarskom stazom, pogledom na planine i toplim večernjim svjetlom',
        'preview_image': 'blog/images/design-previews/staza_prema_vrhovima.png',
    },
    'jedro_u_suton': {
        'label': 'Jedro u suton',
        'description': 'Putopisni tematski dizajn s jedrilicom, zalaskom sunca i jedinstvenim prozirnim panelom za postove i boxeve',
        'preview_image': 'blog/images/design-previews/jedro_u_suton.png',
    },
    'misticno_jezero': {
        'label': 'Mistična laguna',
        'description': 'Tematski dizajn s čarobnim jezerom, lampionima i ljubičastim sjajem',
        'preview_image': 'blog/images/design-previews/misticno_jezero.jpg',
    },
    'dimni_akordi': {
        'label': 'Dimni akordi',
        'description': 'Gradijalni dizajn u toplim bakrenim tonovima inspiriran zadimljenim barom i svjetlom s fotografije.',
        'preview_image': 'blog/images/design-previews/dimni_akordi.png',
    },
    'sjene_ulice': {
        'label': 'Sjene ulice',
        'description': 'Gradijentni noir dizajn s noćnom ulicom, prijelazom iz slike u tamnu pozadinu i toplim lampama.',
        'preview_image': 'blog/images/design-previews/sjene_ulice.png',
    },
    'mjesecev_ples': {
        'label': 'Mjesečev ples',
        'description': 'Gradijentni mistični dizajn s mjesečevim nebom, siluetom i prijelazom u tamni zemljani donji dio.',
        'preview_image': 'blog/images/design-previews/mjesecev_ples.png',
    },
    'asfaltni_plamen': {
        'label': 'Asfaltni plamen',
        'description': 'Gradijentni dizajn s crnim muscle autom, dimom i toplim jantarnim prijelazom u tamni donji dio.',
        'preview_image': 'blog/images/design-previews/asfaltni_plamen.png',
    },
}

DESIGN_TEMPLATE_LABELS = {
    key: value['label']
    for key, value in DESIGN_TEMPLATE_META.items()
}

DESIGN_RIGHT_LAYOUT_TEMPLATES = (
    'default_right',
    'dark_right',
    'classic_right',
)


def get_design_templates():
    return [
        {
            'value': key,
            **value,
        }
        for key, value in DESIGN_TEMPLATE_META.items()
    ]


DESIGN_EDITABLE_FIELDS = (
    'blog_title_font',
    'post_title_font',
    'box_title_font',
    'body_font',
    'blog_title_size',
    'post_title_size',
    'box_title_size',
    'blog_title_color',
    'post_title_color',
    'box_title_color',
    'post_date_color',
    'post_date_style',
    'post_date_effect',
    'post_date_color_1',
    'post_date_color_2',
    'post_date_size',
    'body_text_color',
    'right_box_columns',
    'outer_background_mode',
    'outer_background_color_1',
    'outer_background_color_2',
    'outer_background_pattern',
    'outer_background_image',
    'outer_background_gradient_direction',
    'header_background_mode',
    'header_background_color_1',
    'header_background_color_2',
    'header_background_gradient_direction',
    'content_background_color',
    'content_border_color',
    'box_background_color',
    'box_border_color',
)

DESIGN_RESET_FIELDS = {
    'outer_background': (
        'outer_background_mode',
        'outer_background_color_1',
        'outer_background_color_2',
        'outer_background_pattern',
        'outer_background_image',
        'outer_background_gradient_direction',
    ),
    'header_background': (
        'header_background_mode',
        'header_background_color_1',
        'header_background_color_2',
        'header_background_gradient_direction',
    ),
    'content_boxes': (
        'content_background_color',
        'content_border_color',
        'box_background_color',
        'box_border_color',
    ),
    'blog_title': ('blog_title_font', 'blog_title_color', 'blog_title_size'),
    'post_title': ('post_title_font', 'post_title_color', 'post_title_size'),
    'post_date': ('post_date_style', 'post_date_effect', 'post_date_color_1', 'post_date_color_2', 'post_date_size'),
    'box_title': ('box_title_font', 'box_title_color', 'box_title_size'),
    'body_text': ('body_font', 'body_text_color'),
    'layout': ('right_box_columns',),
}

DESIGN_RESET_LABELS = {
    'outer_background': 'vanjska pozadina',
    'header_background': 'gornja traka',
    'content_boxes': 'sadržaj i boxevi',
    'blog_title': 'naziv bloga',
    'post_title': 'naslov posta',
    'post_date': 'datum posta',
    'box_title': 'naslov boxa',
    'body_text': 'obični tekst',
    'layout': 'raspored boxeva',
}

DESIGN_BACKGROUND_MODE_LABELS = {
    'color': 'Jedna boja',
    'gradient': 'Gradijent',
    'pattern': 'Uzorak',
    'system_image': 'Sistemska slika',
    'upload_image': 'Moja slika',
}

DESIGN_HEADER_MODE_LABELS = {
    'color': 'Jedna boja',
    'gradient': 'Gradijent',
}

POST_DATE_STYLE_CHOICES = [
    {'value': 'classic_vertical', 'label': 'Klasični uspravni'},
    {'value': 'slim_vertical', 'label': 'Tanki uspravni'},
    {'value': 'card', 'label': 'Kartica datum'},
    {'value': 'minimal_inline', 'label': 'Minimalni redni'},
    {'value': 'split', 'label': 'Podijeljeni datum'},
    {'value': 'ribbon', 'label': 'Traka datum'},
    {'value': 'boxed_number', 'label': 'Uokvireni broj'},
    {'value': 'corner_tag', 'label': 'Kutni datum'},
    {'value': 'soft', 'label': 'Rukopisni / soft stil'},
    {'value': 'newspaper', 'label': 'Novinski stil'},
]

POST_DATE_EFFECT_CHOICES = [
    {'value': 'solid', 'label': 'Jednobojni'},
    {'value': 'duo', 'label': 'Dvobojni'},
    {'value': 'gradient', 'label': 'Gradijentni'},
]


def normalize_user_boxes(user):
    for position in ('left', 'right'):
        boxes = UserBox.objects.filter(user=user, position=position).order_by('order', 'id')
        for index, box in enumerate(boxes):
            if box.order != index:
                box.order = index
                box.save(update_fields=['order'])


def get_next_box_order(user, position):
    current_max = UserBox.objects.filter(user=user, position=position).order_by('-order').values_list('order', flat=True).first()
    if current_max is None:
        return 0
    return current_max + 1


def validate_box_layout_counts(layout_items):
    left_count = sum(1 for item in layout_items if item.get('position') == 'left')
    right_count = sum(1 for item in layout_items if item.get('position') == 'right')

    if left_count > MAX_BOXES_PER_SIDE or right_count > MAX_BOXES_PER_SIDE:
        return False

    return True


def validate_blog_banner(upload):
    if not upload:
        return None

    if upload.size > MAX_BLOG_BANNER_SIZE:
        return 'Banner slika je prevelika. Maksimalna veličina je 2 MB.'

    try:
        image = Image.open(upload)
        width, height = image.size
        upload.seek(0)
    except (UnidentifiedImageError, OSError, ValueError):
        try:
            upload.seek(0)
        except Exception:
            pass
        return 'Banner slika nije ispravna slikovna datoteka.'

    if width > MAX_BLOG_BANNER_WIDTH or height > MAX_BLOG_BANNER_HEIGHT:
        return (
            'Banner slika je prevelikih dimenzija. '
            f'Maksimalno je dopušteno {MAX_BLOG_BANNER_WIDTH} x {MAX_BLOG_BANNER_HEIGHT} px.'
        )

    return None


def validate_design_background_upload(upload):
    if not upload:
        return None

    if upload.size > 2 * 1024 * 1024:
        return 'Pozadinska slika je prevelika. Maksimalna veličina je 2 MB.'

    try:
        image = Image.open(upload)
        image.verify()
        upload.seek(0)
    except (UnidentifiedImageError, OSError, ValueError):
        try:
            upload.seek(0)
        except Exception:
            pass
        return 'Pozadinska slika nije ispravna slikovna datoteka.'

    return None


def validate_custom_cursor_upload(upload):
    if not upload:
        return None

    extension = os.path.splitext(upload.name or '')[1].lower()
    if extension not in ALLOWED_CUSTOM_CURSOR_EXTENSIONS:
        return 'Za vlastiti kursor koristi PNG, SVG, WEBP ili CUR.'

    if upload.size > MAX_CUSTOM_CURSOR_SIZE:
        return 'Datoteka za kursor je prevelika. Maksimalna veličina je 512 KB.'

    if extension == '.svg':
        try:
            upload.seek(0)
            sample = upload.read(4096).decode('utf-8', errors='ignore').lower()
            upload.seek(0)
        except Exception:
            return 'SVG kursor nije moguće pročitati.'
        if '<svg' not in sample:
            return 'SVG kursor nije ispravna SVG datoteka.'
        return None

    if extension == '.cur':
        return None

    try:
        image = Image.open(upload)
        width, height = image.size
        upload.seek(0)
    except (UnidentifiedImageError, OSError, ValueError):
        try:
            upload.seek(0)
        except Exception:
            pass
        return 'Datoteka kursora nije ispravna slikovna datoteka.'

    if width > 128 or height > 128:
        return 'Kursor slika je prevelika. Preporuka je do 128 x 128 px.'

    return None



def _delete_custom_cursor_file(relative_path):
    relative_path = str(relative_path or '').strip().lstrip('/')
    if not relative_path:
        return

    absolute_path = os.path.join(settings.MEDIA_ROOT, relative_path)
    if os.path.isfile(absolute_path):
        try:
            os.remove(absolute_path)
        except OSError:
            pass



def _save_custom_cursor_file(user, upload):
    extension = os.path.splitext(upload.name or '')[1].lower()
    filename = f"{uuid.uuid4().hex}{extension}"
    relative_dir = os.path.join('blog', 'custom-cursors', str(user.id))
    absolute_dir = os.path.join(settings.MEDIA_ROOT, relative_dir)
    os.makedirs(absolute_dir, exist_ok=True)
    absolute_path = os.path.join(absolute_dir, filename)

    with open(absolute_path, 'wb+') as destination:
        for chunk in upload.chunks():
            destination.write(chunk)

    return os.path.join(relative_dir, filename).replace('\\', '/')


def _normalize_publish_at(value):
    if not value:
        return None
    try:
        parsed = timezone.datetime.strptime(value, '%Y-%m-%dT%H:%M')
    except (TypeError, ValueError):
        return None
    return timezone.make_aware(parsed, timezone.get_current_timezone())


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


def _first_form_error(form, default_message='Molimo popunite sva obavezna polja.'):
    for field_errors in form.errors.values():
        if field_errors:
            return field_errors[0]
    return default_message


def _build_statistics_context(user):
    now = timezone.now()
    today = timezone.localdate()
    since_7 = now - timedelta(days=7)
    since_30 = now - timedelta(days=30)
    since_90 = now - timedelta(days=90)

    active_posts_qs = Post.objects.filter(author=user).exclude(status='deleted')
    published_posts_qs = active_posts_qs.filter(status='published')

    posts_with_counts = list(
        active_posts_qs
        .select_related('category')
        .annotate(
            like_count=Count('likes', distinct=True),
            comment_count=Count('comments', distinct=True),
            quiz_answer_count=Count('quiz_answers', distinct=True),
            poll_vote_count=Count('poll_votes', distinct=True),
        )
        .order_by('-views', '-created_at')
    )

    published_posts = [post for post in posts_with_counts if post.status == 'published']
    quiz_posts = [post for post in posts_with_counts if post.post_type == 'quiz']
    poll_posts = [post for post in posts_with_counts if post.post_type == 'poll']

    total_posts = len(posts_with_counts)
    published_count = sum(1 for post in posts_with_counts if post.status == 'published')
    draft_count = sum(1 for post in posts_with_counts if post.status == 'draft')
    scheduled_count = sum(1 for post in posts_with_counts if post.status == 'scheduled')

    total_views = sum(post.views or 0 for post in posts_with_counts)
    total_likes = sum(post.like_count for post in posts_with_counts)
    total_comments = sum(post.comment_count for post in posts_with_counts)
    total_followers = Follow.objects.filter(following=user).count()
    total_quiz_answers = sum(post.quiz_answer_count for post in quiz_posts)
    total_poll_votes = sum(post.poll_vote_count for post in poll_posts)

    total_interactions = total_likes + total_comments
    engagement_rate = round((total_interactions / total_views) * 100, 2) if total_views else 0
    avg_views_per_published = round(total_views / published_count, 1) if published_count else 0
    avg_likes_per_published = round(total_likes / published_count, 1) if published_count else 0
    avg_comments_per_published = round(total_comments / published_count, 1) if published_count else 0

    category_stats_map = defaultdict(lambda: {
        'name': 'Bez kategorije',
        'post_count': 0,
        'views': 0,
        'likes': 0,
        'comments': 0,
        'engagement': 0,
    })

    for post in posts_with_counts:
        category_name = post.category.name if post.category else 'Bez kategorije'
        item = category_stats_map[category_name]
        item['name'] = category_name
        item['post_count'] += 1
        item['views'] += post.views or 0
        item['likes'] += post.like_count
        item['comments'] += post.comment_count

    top_categories = list(category_stats_map.values())
    for item in top_categories:
        interactions = item['likes'] + item['comments']
        item['engagement'] = round((interactions / item['views']) * 100, 2) if item['views'] else 0

    top_categories.sort(key=lambda item: (-item['views'], -item['likes'], -item['post_count'], item['name'].lower()))
    top_categories = top_categories[:5]

    top_posts = sorted(
        published_posts,
        key=lambda post: (-(post.views or 0), -post.like_count, -post.comment_count, -post.id),
    )[:5]

    followers_7 = Follow.objects.filter(following=user, created_at__gte=since_7).count()
    followers_30 = Follow.objects.filter(following=user, created_at__gte=since_30).count()
    followers_90 = Follow.objects.filter(following=user, created_at__gte=since_90).count()
    comments_30 = Comment.objects.filter(post__author=user, created_at__gte=since_30).exclude(post__status='deleted').count()
    quiz_answers_30 = QuizAnswer.objects.filter(post__author=user, created_at__gte=since_30).exclude(post__status='deleted').count()
    poll_votes_30 = PollVote.objects.filter(post__author=user, created_at__gte=since_30).exclude(post__status='deleted').count()
    posts_30 = active_posts_qs.filter(created_at__gte=since_30).count()

    quiz_correct_answers = QuizAnswer.objects.filter(
        post__author=user,
        selected_option__is_correct=True,
    ).exclude(post__status='deleted').count()
    quiz_success_rate = round((quiz_correct_answers / total_quiz_answers) * 100, 2) if total_quiz_answers else 0

    top_quiz = None
    if quiz_posts:
        top_quiz = max(quiz_posts, key=lambda post: (post.quiz_answer_count, post.views or 0, post.id))

    top_poll = None
    if poll_posts:
        top_poll = max(poll_posts, key=lambda post: (post.poll_vote_count, post.views or 0, post.id))

    content_type_stats = [
        {
            'label': 'Postovi',
            'count': sum(1 for post in posts_with_counts if post.post_type == 'post'),
            'views': sum((post.views or 0) for post in posts_with_counts if post.post_type == 'post'),
        },
        {
            'label': 'Kvizovi',
            'count': len(quiz_posts),
            'views': sum(post.views or 0 for post in quiz_posts),
        },
        {
            'label': 'Ankete',
            'count': len(poll_posts),
            'views': sum(post.views or 0 for post in poll_posts),
        },
    ]

    chart_days = [today - timedelta(days=offset) for offset in range(13, -1, -1)]
    chart_values_map = {day: 0 for day in chart_days}

    for post in published_posts:
        publication_dt = post.publish_at or post.created_at
        if timezone.is_naive(publication_dt):
            publication_dt = timezone.make_aware(publication_dt, timezone.get_current_timezone())
        publication_day = timezone.localtime(publication_dt).date()
        if publication_day in chart_values_map:
            chart_values_map[publication_day] += post.views or 0

    chart_values = [chart_values_map[day] for day in chart_days]
    chart_max = max(chart_values) if any(chart_values) else 1
    chart_points = []
    if len(chart_values) == 1:
        chart_points.append('50,55')
    else:
        for index, value in enumerate(chart_values):
            x = round((100 / (len(chart_values) - 1)) * index, 2)
            y = round(55 - ((value / chart_max) * 48), 2)
            chart_points.append(f'{x},{y}')

    chart_labels = []
    for index, day in enumerate(chart_days):
        if index in {0, 3, 6, 9, 13}:
            chart_labels.append({
                'index': index,
                'label': day.strftime('%d.%m.'),
            })

    return {
        'total_posts': total_posts,
        'published_count': published_count,
        'draft_count': draft_count,
        'scheduled_count': scheduled_count,
        'total_views': total_views,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'total_followers': total_followers,
        'engagement_rate': engagement_rate,
        'avg_views_per_published': avg_views_per_published,
        'avg_likes_per_published': avg_likes_per_published,
        'avg_comments_per_published': avg_comments_per_published,
        'followers_7': followers_7,
        'followers_30': followers_30,
        'followers_90': followers_90,
        'posts_30': posts_30,
        'comments_30': comments_30,
        'quiz_answers_30': quiz_answers_30,
        'poll_votes_30': poll_votes_30,
        'top_categories': top_categories,
        'top_posts': top_posts,
        'content_type_stats': content_type_stats,
        'quiz_count': len(quiz_posts),
        'poll_count': len(poll_posts),
        'total_quiz_answers': total_quiz_answers,
        'total_poll_votes': total_poll_votes,
        'avg_quiz_answers': round(total_quiz_answers / len(quiz_posts), 1) if quiz_posts else 0,
        'avg_poll_votes': round(total_poll_votes / len(poll_posts), 1) if poll_posts else 0,
        'quiz_success_rate': quiz_success_rate,
        'top_quiz': top_quiz,
        'top_poll': top_poll,
        'chart_points': ' '.join(chart_points),
        'chart_values': chart_values,
        'chart_labels': chart_labels,
        'chart_max': chart_max,
        'chart_has_real_view_history': False,
    }


@staff_member_required
def update_site_message(request):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return HttpResponseForbidden('Nemaš ovlasti.')

    if request.method == 'POST':
        
        msg, _ = SiteMessage.objects.get_or_create(id=1)
        msg.content_html = request.POST.get('content_html', '')
        if request.POST.get('remove_image') == '1' and msg.image:
            msg.image.delete(save=False)
            msg.image = None
        if 'image' in request.FILES:
            msg.image = request.FILES['image']
        msg.save()
        messages.success(request, 'Poruka je spremljena.')
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def add_box(request):
    normalize_user_boxes(request.user)
    left_count = UserBox.objects.filter(user=request.user, position='left').count()
    right_count = UserBox.objects.filter(user=request.user, position='right').count()

    if request.method == 'POST':
        form = UserBoxForm(request.POST)
        if form.is_valid():
            position = form.cleaned_data['position']

            if position == 'left' and left_count >= MAX_BOXES_PER_SIDE:
                messages.error(request, f'Ne možeš dodati više od {MAX_BOXES_PER_SIDE} lijeva boxa.')
                return redirect('/blog/settings/?tab=boxevi')

            if position == 'right' and right_count >= MAX_BOXES_PER_SIDE:
                messages.error(request, f'Ne možeš dodati više od {MAX_BOXES_PER_SIDE} desna boxa.')
                return redirect('/blog/settings/?tab=boxevi')

            box = form.save(commit=False)
            box.user = request.user
            box.order = get_next_box_order(request.user, position)
            box.save()
            return redirect(f'/blog/settings/?tab=boxevi&box={box.id}')
    else:
        form = UserBoxForm()

    return render(request, 'blog/add_box.html', {
        'form': form,
        'left_count': left_count,
        'right_count': right_count,
        'max_boxes_per_side': MAX_BOXES_PER_SIDE,
        'box_title_limit': UserBoxForm.MAX_TITLE_LENGTH,
        'box_content_limit': UserBoxForm.MAX_CONTENT_LENGTH,
    })


@login_required
def edit_box(request, box_id):
    normalize_user_boxes(request.user)
    box = get_object_or_404(UserBox, id=box_id, user=request.user)

    if request.method == 'POST':
        form = UserBoxForm(request.POST, instance=box)
        if form.is_valid():
            new_position = form.cleaned_data.get('position')
            old_position = box.position

            left_count = UserBox.objects.filter(user=request.user, position='left').exclude(id=box.id).count()
            right_count = UserBox.objects.filter(user=request.user, position='right').exclude(id=box.id).count()

            if new_position == 'left' and left_count >= MAX_BOXES_PER_SIDE:
                messages.error(request, f'Ne možeš prebaciti box lijevo jer je lijeva strana puna (max {MAX_BOXES_PER_SIDE}).')
                return redirect(f'/blog/settings/?tab=boxevi&box={box.id}')

            if new_position == 'right' and right_count >= MAX_BOXES_PER_SIDE:
                messages.error(request, f'Ne možeš prebaciti box desno jer je desna strana puna (max {MAX_BOXES_PER_SIDE}).')
                return redirect(f'/blog/settings/?tab=boxevi&box={box.id}')

            updated_box = form.save(commit=False)

            if old_position != new_position:
                updated_box.order = get_next_box_order(request.user, new_position)

            updated_box.save()
            normalize_user_boxes(request.user)
            return redirect(f'/blog/settings/?tab=boxevi&box={box.id}')

        for field_errors in form.errors.values():
            for error in field_errors:
                messages.error(request, error)

        return redirect(f'/blog/settings/?tab=boxevi&box={box.id}')
    else:
        form = UserBoxForm(instance=box)

    return render(request, 'blog/edit_box.html', {'form': form})


@login_required
def delete_box(request, box_id):
    box = get_object_or_404(UserBox, id=box_id, user=request.user)
    if request.method == 'POST':
        box.delete()
        normalize_user_boxes(request.user)
        return redirect('/blog/settings/?tab=boxevi')
    return render(request, 'blog/delete_box.html', {'box': box})


@login_required
def blog_settings(request):
    publish_due_posts(request.user)
    profile = request.user.profile
    normalize_user_boxes(request.user)
    boxes = UserBox.objects.filter(user=request.user).order_by('position', 'order', 'id')
    left_boxes = list(boxes.filter(position='left'))
    right_boxes = list(boxes.filter(position='right'))
    left_count = len(left_boxes)
    right_count = len(right_boxes)
    box_id = request.GET.get('box')
    active_box = boxes.filter(id=box_id).first() if box_id else boxes.first()
    active_box_form = UserBoxForm(instance=active_box) if active_box else None

    post_filter = request.GET.get('post_filter', 'published')
    post_id = request.GET.get('post_id')
    edit_post = None
    user_posts = None
    post_form = PostForm()

    settings_tab = request.GET.get('settings_tab', 'opcenito')
    design_tab = request.GET.get('design_tab', 'predlosci')

    blocked_users = (
        UserBlock.objects
        .filter(blocker=request.user)
        .select_related("blocked", "blocked__profile")
        .order_by("blocked__username")
    )

    restricted_users = (
        UserRestriction.objects
        .filter(owner=request.user)
        .select_related("restricted", "restricted__profile")
        .order_by("restricted__username")
    )

    author_form = AuthorProfileForm(instance=profile)
    author_question_filter = request.GET.get('author_question_filter', 'all')
    author_questions_base = (
        AuthorQuestion.objects
        .filter(author=request.user)
        .select_related('sender', 'sender__profile')
        .order_by('-created_at')
    )

    author_questions_all_count = author_questions_base.count()
    author_questions_answered_count = author_questions_base.exclude(answer='').count()
    author_questions_unanswered_count = author_questions_base.filter(answer='').count()

    received_author_questions = author_questions_base
    if author_question_filter == 'answered':
        received_author_questions = author_questions_base.exclude(answer='')
    elif author_question_filter == 'unanswered':
        received_author_questions = author_questions_base.filter(answer='')
    else:
        author_question_filter = 'all'

    author_tab_redirect = f'/blog/settings/?tab=autor&author_question_filter={author_question_filter}'

    if request.method == 'POST':

        if request.GET.get('tab') == 'autor' and 'save_author_profile' in request.POST:
            author_form = AuthorProfileForm(request.POST, instance=profile)
            if author_form.is_valid():
                author_form.save()
                messages.success(request, 'Podaci za Upoznaj autora su spremljeni.')
            else:
                first_error = next(iter(author_form.errors.values()))[0] if author_form.errors else 'Provjeri unesene podatke.'
                messages.error(request, first_error)
            return redirect(author_tab_redirect)

        if request.GET.get('tab') == 'autor' and 'save_author_question' in request.POST:
            question = AuthorQuestion.objects.filter(id=request.POST.get('author_question_id'), author=request.user).first()
            if question:
                answer = (request.POST.get('answer') or '').strip()
                question.answer = answer
                question.is_public = bool(answer) and request.POST.get('is_public') == '1'
                question.answered_at = timezone.now() if answer else None
                question.save(update_fields=['answer', 'is_public', 'answered_at'])
                messages.success(request, 'Pitanje autora je spremljeno.')
            else:
                messages.error(request, 'Pitanje nije pronađeno.')
            return redirect(author_tab_redirect)

        if request.GET.get('tab') == 'autor' and 'delete_author_question' in request.POST:
            question = AuthorQuestion.objects.filter(id=request.POST.get('author_question_id'), author=request.user).first()
            if question:
                question.delete()
                messages.success(request, 'Pitanje je izbrisano.')
            else:
                messages.error(request, 'Pitanje nije pronađeno.')
            return redirect(author_tab_redirect)

                # --- ODBLOKIRAJ KORISNIKA ---
        if "unblock_user_id" in request.POST:
            unblock_user_id = request.POST.get("unblock_user_id")

            block_relation = (
                UserBlock.objects
                .filter(blocker=request.user, blocked_id=unblock_user_id)
                .select_related("blocked")
                .first()
            )

            if block_relation:
                blocked_username = block_relation.blocked.username
                block_relation.delete()
                messages.success(request, f"Odblokirao si korisnika {blocked_username}.")
            else:
                messages.error(request, "Korisnik nije pronađen u listi blokiranih.")

            return redirect("/blog/settings/?tab=postavke&settings_tab=sigurnost")

        if "remove_restriction_user_id" in request.POST:
            restricted_user_id = request.POST.get("remove_restriction_user_id")

            restriction_relation = (
                UserRestriction.objects
                .filter(owner=request.user, restricted_id=restricted_user_id)
                .select_related("restricted")
                .first()
            )

            if restriction_relation:
                restricted_username = restriction_relation.restricted.username
                restriction_relation.delete()
                messages.success(request, f"Maknuo si ograničenje za korisnika {restricted_username}.")
            else:
                messages.error(request, "Korisnik nije pronađen u listi ograničenih.")

            return redirect("/blog/settings/?tab=postavke&settings_tab=sigurnost")

        if 'save_box_layout' in request.POST:
            raw_layout = request.POST.get('box_layout_json', '[]')

            try:
                layout = json.loads(raw_layout)
            except json.JSONDecodeError:
                messages.error(request, 'Raspored boxeva nije ispravan.')
                return redirect('/blog/settings/?tab=boxevi')

            if not isinstance(layout, list):
                messages.error(request, 'Raspored boxeva nije ispravan.')
                return redirect('/blog/settings/?tab=boxevi')

            cleaned_layout = []
            seen_ids = set()
            user_box_ids = set(UserBox.objects.filter(user=request.user).values_list('id', flat=True))

            for item in layout:
                if not isinstance(item, dict):
                    continue

                try:
                    box_id = int(item.get('id'))
                except (TypeError, ValueError):
                    continue

                position = item.get('position')
                if position not in {'left', 'right'}:
                    continue

                if box_id in seen_ids or box_id not in user_box_ids:
                    continue

                seen_ids.add(box_id)
                cleaned_layout.append({'id': box_id, 'position': position})

            if len(cleaned_layout) != len(user_box_ids):
                messages.error(request, 'Nisu spremljeni svi boxevi. Pokušaj ponovno.')
                return redirect('/blog/settings/?tab=boxevi')

            if not validate_box_layout_counts(cleaned_layout):
                messages.error(request, f'Na svakoj strani mogu biti najviše {MAX_BOXES_PER_SIDE} boxa.')
                return redirect('/blog/settings/?tab=boxevi')

            grouped = {'left': [], 'right': []}
            for item in cleaned_layout:
                grouped[item['position']].append(item['id'])

            for position in ('left', 'right'):
                for order, box_id in enumerate(grouped[position]):
                    UserBox.objects.filter(id=box_id, user=request.user).update(position=position, order=order)

            normalize_user_boxes(request.user)

            target_box_id = request.POST.get('active_box_id')
            if target_box_id and str(target_box_id).isdigit() and int(target_box_id) in user_box_ids:
                messages.success(request, 'Raspored boxeva je spremljen.')
                return redirect(f'/blog/settings/?tab=boxevi&box={int(target_box_id)}')

            messages.success(request, 'Raspored boxeva je spremljen.')
            return redirect('/blog/settings/?tab=boxevi')

        if 'bulk_restore' in request.POST or 'bulk_permanent_delete' in request.POST:
            selected_ids = request.POST.getlist('selected_posts')
            if not selected_ids:
                messages.error(request, 'Niste označili nijedan post.')
                return redirect('/blog/settings/?tab=postovi&post_filter=deleted')
            posts_qs = Post.objects.filter(id__in=selected_ids, author=request.user, status='deleted')
            if 'bulk_restore' in request.POST:
                posts_qs.update(status='draft')
                return redirect('/blog/settings/?tab=postovi&post_filter=draft')
            deleted_posts = []
            for post in posts_qs:
                deleted_posts.append({'id': post.id, 'title': post.title})
                if post.image:
                    post.image.delete(save=False)
                for img in post.images.all():
                    if img.image:
                        img.image.delete(save=False)
                    img.delete()
                post.delete()
            if deleted_posts:
                log_security_event(
                    request,
                    event_type='post_deleted',
                    user=request.user,
                    severity='warning',
                    message='Korisnik je trajno izbrisao više postova iz otpada.',
                    metadata={'posts': deleted_posts},
                )
            return redirect('/blog/settings/?tab=postovi&post_filter=deleted')

        if 'create_quiz' in request.POST or 'save_quiz_draft' in request.POST:
            question = request.POST.get('question', '').strip()
            options = [o.strip() for o in request.POST.getlist('quiz_option') if o.strip()]
            correct_index = request.POST.get('correct_option')
            allow_comments = request.POST.get('allow_comments') == 'on'
            submit_action = 'draft' if 'save_quiz_draft' in request.POST else 'publish'
            publish_at = _normalize_publish_at(request.POST.get('publish_at')) if submit_action == 'publish' else None
            if not question:
                messages.error(request, 'Pitanje je obavezno.')
                return redirect('/blog/settings/?tab=postovi&post_filter=quiz_new')
            if len(options) < 2:
                messages.error(request, 'Dodaj barem 2 odgovora.')
                return redirect('/blog/settings/?tab=postovi&post_filter=quiz_new')
            if correct_index in (None, ''):
                messages.error(request, 'Moraš označiti točan odgovor.')
                return redirect('/blog/settings/?tab=postovi&post_filter=quiz_new')
            if submit_action == 'publish' and request.POST.get('publish_at') and not publish_at:
                messages.error(request, 'Upiši ispravan datum i vrijeme objave.')
                return redirect('/blog/settings/?tab=postovi&post_filter=quiz_new')
            if publish_at and publish_at <= timezone.now():
                messages.error(request, 'Vrijeme objave mora biti u budućnosti ili ostavi polje prazno za objavu odmah.')
                return redirect('/blog/settings/?tab=postovi&post_filter=quiz_new')
            correct_index = int(correct_index)
            category = Category.objects.filter(name__iexact='Kviz').first()
            if not category:
                messages.error(request, 'Ne postoji kategorija "Kviz".')
                return redirect('/blog/settings/?tab=postovi&post_filter=quiz_new')
            post = Post(author=request.user, title=question, content='', category=category, post_type='quiz')
            post.allow_comments = allow_comments
            _apply_submit_action_to_post(post, submit_action, publish_at)
            if request.FILES.get('image'):
                post.image = request.FILES['image']
            if post.status == 'published':
                assign_home_image(post)
            post.save()
            for i, text in enumerate(options):
                QuizOption.objects.create(post=post, text=text, is_correct=(i == correct_index))
            return redirect(f'/blog/settings/?tab=postovi&post_filter={post.status}')

        if 'create_poll' in request.POST or 'save_poll_draft' in request.POST:
            question = request.POST.get('question', '').strip()
            options = [o.strip() for o in request.POST.getlist('poll_option') if o.strip()]
            allow_comments = request.POST.get('allow_comments') == 'on'
            submit_action = 'draft' if 'save_poll_draft' in request.POST else 'publish'
            publish_at = _normalize_publish_at(request.POST.get('publish_at')) if submit_action == 'publish' else None
            if not question:
                messages.error(request, 'Pitanje ankete je obavezno.')
                return redirect('/blog/settings/?tab=postovi&post_filter=poll_new')
            if len(options) < 2:
                messages.error(request, 'Dodaj barem 2 opcije.')
                return redirect('/blog/settings/?tab=postovi&post_filter=poll_new')
            if submit_action == 'publish' and request.POST.get('publish_at') and not publish_at:
                messages.error(request, 'Upiši ispravan datum i vrijeme objave.')
                return redirect('/blog/settings/?tab=postovi&post_filter=poll_new')
            if publish_at and publish_at <= timezone.now():
                messages.error(request, 'Vrijeme objave mora biti u budućnosti ili ostavi polje prazno za objavu odmah.')
                return redirect('/blog/settings/?tab=postovi&post_filter=poll_new')
            category = Category.objects.filter(name__iexact='Anketa').first()
            if not category:
                messages.error(request, 'Ne postoji kategorija "Anketa".')
                return redirect('/blog/settings/?tab=postovi&post_filter=poll_new')
            post = Post(author=request.user, title=question, content='', category=category, post_type='poll')
            post.allow_comments = allow_comments
            _apply_submit_action_to_post(post, submit_action, publish_at)
            if request.FILES.get('image'):
                post.image = request.FILES['image']
            if post.status == 'published':
                assign_home_image(post)
            post.save()
            for text in options:
                PollOption.objects.create(post=post, text=text)
            return redirect(f'/blog/settings/?tab=postovi&post_filter={post.status}')

        if 'permanent_delete_id' in request.POST:
            post = Post.objects.filter(id=request.POST.get('permanent_delete_id'), author=request.user).first()
            if post:
                post_meta = {'post_id': post.id, 'post_title': post.title}
                if post.image:
                    post.image.delete(save=False)
                for img in post.images.all():
                    if img.image:
                        img.image.delete(save=False)
                    img.delete()
                post.delete()
                log_security_event(
                    request,
                    event_type='post_deleted',
                    user=request.user,
                    severity='warning',
                    message='Korisnik je trajno izbrisao post iz otpada.',
                    metadata=post_meta,
                )
            return redirect('/blog/settings/?tab=postovi&post_filter=deleted')

        if 'restore_post_id' in request.POST:
            post = Post.objects.filter(id=request.POST.get('restore_post_id'), author=request.user).first()
            if post:
                post.status = 'draft'
                post.save()
            return redirect('/blog/settings/?tab=postovi&post_filter=draft')

        if 'delete_post_id' in request.POST:
            post = Post.objects.filter(id=request.POST.get('delete_post_id'), author=request.user).first()
            if post:
                post.status = 'deleted'
                post.save()
                log_security_event(
                    request,
                    event_type='post_deleted',
                    user=request.user,
                    severity='info',
                    message='Korisnik je premjestio post u otpad.',
                    metadata={'post_id': post.id, 'post_title': post.title},
                )
            return redirect('/blog/settings/?tab=postovi&post_filter=published')

        if 'update_post_id' in request.POST:
            post = Post.objects.filter(id=request.POST.get('update_post_id'), author=request.user).first()
            if post:
                form = PostForm(request.POST, request.FILES, instance=post)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.category = Category.objects.filter(id=request.POST.get('category')).first()
                    post.allow_comments = form.cleaned_data.get('allow_comments', True)
                    submit_action = 'publish'
                    if request.POST.get('save_as_draft') == '1':
                        submit_action = 'draft'
                    publish_at = form.cleaned_data.get('publish_at') if submit_action == 'publish' else None
                    if request.POST.get('delete_image') and post.image:
                        post.image.delete(save=False)
                        post.image = None
                    _apply_submit_action_to_post(post, submit_action, publish_at)
                    if post.status == 'published':
                        assign_home_image(post)
                    delete_ids = request.POST.getlist('delete_post_images')
                    if delete_ids:
                        imgs = PostImage.objects.filter(id__in=delete_ids, post=post)
                        for img in imgs:
                            if img.image:
                                img.image.delete(save=False)
                            img.delete()
                    post.save()
                    apply_tags_to_post(post, form.cleaned_data.get('tags_list', []))
                    for upload in request.FILES.getlist('images'):
                        PostImage.objects.create(post=post, image=upload)
                    return redirect(f'/blog/settings/?tab=postovi&post_filter={post.status}')
                messages.error(request, _first_form_error(form))
                return redirect(f'/blog/settings/?tab=postovi&post_filter=edit&post_id={post.id}')

        if 'publish_post' in request.POST or 'save_draft' in request.POST:
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.category = Category.objects.filter(id=request.POST.get('category')).first()
                post.post_type = 'post'
                post.allow_comments = form.cleaned_data.get('allow_comments', True)

                submit_action = 'draft' if 'save_draft' in request.POST else 'publish'
                publish_at = form.cleaned_data.get('publish_at') if submit_action == 'publish' else None
                _apply_submit_action_to_post(post, submit_action, publish_at)

                if submit_action == 'publish' and not post.category:
                    messages.error(request, 'Morate odabrati kategoriju prije objave.')
                    post_filter = 'new'
                    post_form = form
                else:
                    if post.status == 'published':
                        assign_home_image(post)
                    post.save()
                    apply_tags_to_post(post, form.cleaned_data.get('tags_list', []))
                    for upload in request.FILES.getlist('images'):
                        PostImage.objects.create(post=post, image=upload)
                    return redirect(f'/blog/settings/?tab=postovi&post_filter={post.status}')
            else:
                messages.error(request, _first_form_error(form))
                post_filter = 'new'
                post_form = form

        if 'design' in request.POST:
            selected_design = request.POST.get('design')
            if selected_design in DESIGN_TEMPLATE_LABELS:
                profile.template = selected_design
                profile.save(update_fields=['template'])
            return redirect('/blog/settings/?tab=dizajn&design_tab=predlosci')

        if 'save_design_customization' in request.POST:
            active_template = profile.template if profile.template in DESIGN_TEMPLATE_LABELS else 'default'
            current_preferences = get_blog_preferences(request.user)
            design_customizations = normalize_design_customizations(
                current_preferences.get('design_customizations')
            )
            current_design = design_customizations.get(active_template, {}).copy()
            default_designs = normalize_design_customizations(None)
            default_active_design = default_designs[active_template]
            reset_part = request.POST.get('reset_design_part')
            reset_field = request.POST.get('reset_design_field')
            reset_all = request.POST.get('reset_design_all') == '1'

            if reset_all:
                current_design = default_active_design.copy()
                messages.success(request, 'Sve postavke ovog dizajna vraćene su na default.')
            elif reset_field in DESIGN_EDITABLE_FIELDS:
                current_design[reset_field] = default_active_design[reset_field]
                messages.success(request, 'Odabrana stavka vraćena je na default.')
            elif reset_part in DESIGN_RESET_FIELDS:
                for field_name in DESIGN_RESET_FIELDS[reset_part]:
                    current_design[field_name] = default_active_design[field_name]
                section_label = DESIGN_RESET_LABELS.get(reset_part, 'odabrani dio')
                messages.success(request, f'{section_label.capitalize()} vraćen je na default.')
            else:
                for field_name in DESIGN_EDITABLE_FIELDS:
                    if field_name in request.POST:
                        current_design[field_name] = request.POST.get(field_name)

                if request.POST.get('delete_simple_background_image') == '1' and profile.simple_background_image:
                    profile.simple_background_image.delete(save=False)
                    profile.simple_background_image = None

                if request.FILES.get('simple_background_image'):
                    image_error = validate_design_background_upload(request.FILES['simple_background_image'])
                    if image_error:
                        messages.error(request, image_error)
                        return redirect('/blog/settings/?tab=dizajn&design_tab=uredivanje')

                    if profile.simple_background_image and profile.simple_background_image.name:
                        profile.simple_background_image.delete(save=False)
                    profile.simple_background_image = request.FILES['simple_background_image']

                profile.save()
                messages.success(request, 'Uređivanje dizajna je spremljeno.')

            design_customizations[active_template] = current_design
            set_blog_preferences(request.user, {
                'design_customizations': design_customizations,
            })
            return redirect('/blog/settings/?tab=dizajn&design_tab=uredivanje')


        if request.GET.get('tab') == 'dizajn' and design_tab == 'ugodaj':
            allowed_cursor_values = {item['value'] for item in get_blog_cursor_choices()}
            allowed_cursor_effect_values = {item['value'] for item in get_blog_cursor_effect_choices()}
            allowed_music_values = {item['id'] for item in get_ambient_music_tracks()}
            selected_cursor_style = str(request.POST.get('cursor_style', 'default') or 'default').strip()
            selected_cursor_effect = str(request.POST.get('cursor_effect', 'none') or 'none').strip()
            ambient_music_enabled = request.POST.get('ambient_music_enabled') == '1'
            ambient_music_track = str(request.POST.get('ambient_music_track', '') or '').strip()

            try:
                ambient_music_volume = int(request.POST.get('ambient_music_volume', 18) or 18)
            except Exception:
                ambient_music_volume = 18
            ambient_music_volume = max(0, min(100, ambient_music_volume))

            if selected_cursor_style not in allowed_cursor_values:
                selected_cursor_style = 'default'

            if selected_cursor_effect not in allowed_cursor_effect_values:
                selected_cursor_effect = 'none'

            if ambient_music_track not in allowed_music_values:
                ambient_music_track = ''

            if ambient_music_track == '':
                ambient_music_enabled = False

            set_blog_preferences(request.user, {
                'cursor_style': selected_cursor_style,
                'cursor_effect': selected_cursor_effect,
                'ambient_music_enabled': ambient_music_enabled,
                'ambient_music_track': ambient_music_track,
                'ambient_music_volume': ambient_music_volume,
            })
            messages.success(request, 'Kursor, efekt i glazba bloga su spremljeni.')
            return redirect('/blog/settings/?tab=dizajn&design_tab=ugodaj')

        if request.GET.get('tab') == 'postavke':
            settings_changed = False
            banner_changed = False
            updated_preferences = {}

            if settings_tab == 'opcenito':
                blog_tagline = (request.POST.get('blog_tagline') or '').strip()
                if len(blog_tagline) > 220:
                    messages.error(request, 'Kratka poruka bloga može imati najviše 220 znakova.')
                    return redirect(f'/blog/settings/?tab=postavke&settings_tab={settings_tab}')

                if profile.blog_tagline != blog_tagline:
                    profile.blog_tagline = blog_tagline
                    settings_changed = True

                if request.POST.get('delete_avatar') == '1':
                    if profile.avatar:
                        profile.avatar.delete(save=False)
                        profile.avatar = None
                        settings_changed = True

                cropped_image_data = request.POST.get('cropped_image')
                if cropped_image_data:
                    try:
                        image_format, imgstr = cropped_image_data.split(';base64,')
                        ext = image_format.split('/')[-1]
                        file = ContentFile(base64.b64decode(imgstr), name=f'avatar.{ext}')
                    except (ValueError, TypeError, base64.binascii.Error):
                        messages.error(request, 'Avatar nije moguće spremiti. Pokušaj ponovno.')
                        return redirect(f'/blog/settings/?tab=postavke&settings_tab={settings_tab}')

                    if profile.avatar and profile.avatar.path and os.path.isfile(profile.avatar.path):
                        os.remove(profile.avatar.path)

                    profile.avatar = file
                    settings_changed = True

                selected_position = request.POST.get('blog_banner_position')
                if selected_position in {'left', 'center', 'right'} and profile.blog_banner_position != selected_position:
                    profile.blog_banner_position = selected_position
                    banner_changed = True
                    settings_changed = True

                if request.POST.get('delete_blog_banner') == '1':
                    if profile.blog_banner:
                        profile.blog_banner.delete(save=False)
                    profile.blog_banner = None
                    banner_changed = True
                    settings_changed = True

                if request.FILES.get('blog_banner'):
                    new_banner = request.FILES['blog_banner']
                    banner_error = validate_blog_banner(new_banner)
                    if banner_error:
                        messages.error(request, banner_error)
                        return redirect(f'/blog/settings/?tab=postavke&settings_tab={settings_tab}')

                    if profile.blog_banner and profile.blog_banner.name:
                        profile.blog_banner.delete(save=False)
                    profile.blog_banner = new_banner
                    banner_changed = True
                    settings_changed = True

            elif settings_tab == 'postovi':
                posts_per_page = request.POST.get('posts_per_page')
                if posts_per_page in {'5', '10', '15', '20'}:
                    updated_preferences['posts_per_page'] = int(posts_per_page)

                archive_mode = request.POST.get('blog_archive_mode')
                if archive_mode in {'both', 'calendar', 'list', 'none'}:
                    updated_preferences['blog_archive_mode'] = archive_mode

            elif settings_tab == 'komentari':
                updated_preferences['show_post_comments'] = request.POST.get('show_post_comments', '1') == '1'
                updated_preferences['allow_comments'] = request.POST.get('allow_comments', '1') == '1'

                allow_anonymous_comments = request.POST.get('allow_anonymous_comments', '0') == '1'
                current_allow_anonymous = get_allow_anonymous_comments(request.user)
                if current_allow_anonymous != allow_anonymous_comments:
                    set_allow_anonymous_comments(request.user, allow_anonymous_comments)
                    settings_changed = True

            elif settings_tab == 'posjetitelji':
                updated_preferences.update({
                    'analytics_live_counter_enabled': request.POST.get('analytics_live_counter_enabled') == '1',
                    'analytics_map_enabled': request.POST.get('analytics_map_enabled') == '1',
                    'analytics_geo_enabled': request.POST.get('analytics_geo_enabled') == '1',
                    'analytics_active_pages_enabled': request.POST.get('analytics_active_pages_enabled') == '1',
                })

                widget_side = request.POST.get('analytics_widget_side')
                if widget_side in {'left_top', 'left_bottom', 'right_top', 'right_bottom', 'footer_full'}:
                    updated_preferences['analytics_widget_side'] = widget_side

                map_variant = request.POST.get('analytics_map_variant')
                if map_variant in {'map', 'globe'}:
                    updated_preferences['analytics_map_variant'] = map_variant

                stat_card_size = request.POST.get('analytics_stat_card_size')
                if stat_card_size in {'small', 'medium', 'large'}:
                    updated_preferences['analytics_stat_card_size'] = stat_card_size

            if updated_preferences:
                set_blog_preferences(request.user, updated_preferences)
                settings_changed = True

            if settings_changed:
                profile.save()
                if settings_tab == 'posjetitelji':
                    messages.success(request, 'Postavke za posjetitelje su spremljene.')
                elif banner_changed:
                    messages.success(request, 'Postavke i slika na vrhu bloga su spremljene.')
                else:
                    messages.success(request, 'Postavke bloga su spremljene.')
                return redirect(f'/blog/settings/?tab=postavke&settings_tab={settings_tab}')

    if post_filter == 'edit' and post_id:
        edit_post = Post.objects.filter(id=post_id, author=request.user).first()
    if edit_post:
        post_form = PostForm(instance=edit_post)

    if post_filter == 'published':
        user_posts = annotate_publication_datetime(Post.objects.filter(author=request.user, status='published')).order_by('-publication_datetime_db', '-created_at')
    elif post_filter == 'draft':
        user_posts = Post.objects.filter(author=request.user, status='draft').order_by('-created_at')
    elif post_filter == 'scheduled':
        user_posts = Post.objects.filter(author=request.user, status='scheduled').order_by('publish_at', '-created_at')
    elif post_filter == 'deleted':
        user_posts = Post.objects.filter(author=request.user, status='deleted').order_by('-created_at')

    blog_preferences = apply_blog_preferences_to_profile(profile, request.user)
    design_customizations = blog_preferences.get('design_customizations', {})
    active_design_template = profile.template if profile.template in DESIGN_TEMPLATE_LABELS else 'default'
    active_design_customization = build_design_customization_payload(
        design_customizations.get(
            active_design_template,
            blog_preferences.get('active_design_customization', {}),
        )
    )
    default_design_customizations = normalize_design_customizations(None)
    default_active_design_customization = build_design_customization_payload(
        default_design_customizations.get(active_design_template, {})
    )
    statistics = _build_statistics_context(request.user) if request.GET.get('tab') == 'statistika' else None
    live_analytics = build_live_analytics_context(request.user) if (
        request.GET.get('tab') == 'statistika'
        or (request.GET.get('tab') == 'postavke' and settings_tab == 'posjetitelji')
    ) else None

    return render(request, 'blog/blog_settings.html', {
        'boxes': boxes,
        'left_boxes': left_boxes,
        'right_boxes': right_boxes,
        'left_count': left_count,
        'right_count': right_count,
        'max_boxes_per_side': MAX_BOXES_PER_SIDE,
        'box_title_limit': UserBoxForm.MAX_TITLE_LENGTH,
        'box_content_limit': UserBoxForm.MAX_CONTENT_LENGTH,
        'active_box': active_box,
        'active_box_form': active_box_form,
        'profile': profile,
        'author_form': author_form,
        'received_author_questions': received_author_questions,
        'author_question_filter': author_question_filter,
        'author_questions_all_count': author_questions_all_count,
        'author_questions_answered_count': author_questions_answered_count,
        'author_questions_unanswered_count': author_questions_unanswered_count,
        'user_posts': user_posts,
        'post_filter': post_filter,
        'edit_post': edit_post,
        'categories': Category.objects.all().order_by('group', 'name'),
        'published_count': Post.objects.filter(author=request.user, status='published').count(),
        'draft_count': Post.objects.filter(author=request.user, status='draft').count(),
        'scheduled_count': Post.objects.filter(author=request.user, status='scheduled').count(),
        'deleted_count': Post.objects.filter(author=request.user, status='deleted').count(),
        'post_form': post_form,
        "blocked_users": blocked_users,
        "restricted_users": restricted_users,
        'settings_tab': settings_tab,
        'design_tab': design_tab,
        'design_font_choices': get_design_font_choices(),
        'design_pattern_choices': get_design_pattern_choices(),
        'design_background_image_choices': get_design_background_image_choices(),
        'soho_cover_image_choices': get_soho_cover_image_choices(),
        'design_gradient_direction_choices': get_design_gradient_direction_choices(),
        'design_template_labels': DESIGN_TEMPLATE_LABELS,
        'design_templates': get_design_templates(),
        'design_right_layout_templates': DESIGN_RIGHT_LAYOUT_TEMPLATES,
        'design_background_mode_labels': DESIGN_BACKGROUND_MODE_LABELS,
        'design_header_mode_labels': DESIGN_HEADER_MODE_LABELS,
        'design_font_label_map': {item['value']: item['label'] for item in get_design_font_choices()},
        'design_pattern_label_map': {item['value']: item['label'] for item in get_design_pattern_choices()},
        'design_background_image_label_map': {item['value']: item['label'] for item in get_design_background_image_choices()},
        'design_gradient_direction_label_map': {item['value']: item['label'] for item in get_design_gradient_direction_choices()},
        'active_design_template': active_design_template,
        'active_design_customization': active_design_customization,
        'default_active_design_customization': default_active_design_customization,
        'allow_anonymous_comments': get_allow_anonymous_comments(request.user),
        'cursor_choices': get_blog_cursor_choices(),
        'cursor_effect_choices': get_blog_cursor_effect_choices(),
        'ambient_music_tracks': get_ambient_music_tracks(),
        'ambient_music_categories': get_ambient_music_categories(),
        'blog_preferences': blog_preferences,
        'statistics': statistics,
        'live_analytics': live_analytics,
    })


@login_required
def design_live_editor_titles(request):
    profile = request.user.profile
    blog_preferences = get_blog_preferences(request.user)
    design_customizations = normalize_design_customizations(blog_preferences.get('design_customizations'))
    active_template = profile.template
    current_design = design_customizations.get(active_template, {}).copy()

    title_fields = (
        'blog_title_font', 'blog_title_color', 'blog_title_size',
        'post_title_font', 'post_title_color', 'post_title_size',
        'box_title_font', 'box_title_color', 'box_title_size',
        'post_date_style', 'post_date_effect', 'post_date_color_1', 'post_date_color_2', 'post_date_size',
    )
    background_fields = (
        'outer_background_mode',
        'outer_background_color_1',
        'outer_background_color_2',
        'outer_background_pattern',
        'outer_background_image',
        'outer_background_gradient_direction',
        'header_background_mode',
        'header_background_color_1',
        'header_background_color_2',
        'header_background_gradient_direction',
        'content_background_color',
        'box_background_color',
    )

    default_designs = normalize_design_customizations(None)
    default_active_design_raw = default_designs.get(active_template, {}).copy()
    default_active_design = build_design_customization_payload(default_active_design_raw)

    if str(current_design.get('blog_title_size') or '').strip() == '54':
        current_design['blog_title_size'] = str(default_active_design.get('blog_title_size', '32'))

    if str(current_design.get('post_title_size') or '').strip() == '32':
        current_design['post_title_size'] = str(default_active_design.get('post_title_size', '24'))

    if str(current_design.get('box_title_size') or '').strip() == '24':
        current_design['box_title_size'] = str(default_active_design.get('box_title_size', '13'))

    if not current_design.get('post_date_style'):
        current_design['post_date_style'] = str(default_active_design.get('post_date_style', 'classic_vertical'))
    if not current_design.get('post_date_effect'):
        current_design['post_date_effect'] = str(default_active_design.get('post_date_effect', 'solid'))
    if not current_design.get('post_date_color_1'):
        current_design['post_date_color_1'] = str(default_active_design.get('post_date_color_1', current_design.get('post_date_color') or '#d97706'))
    if not current_design.get('post_date_color_2'):
        current_design['post_date_color_2'] = str(default_active_design.get('post_date_color_2', current_design.get('post_date_color_1') or '#ffd200'))
    if not current_design.get('post_date_size'):
        current_design['post_date_size'] = str(default_active_design.get('post_date_size', '100'))

    supports_background_editor = is_simple_design_template(active_template)
    allowed_background_modes = []
    if active_template == 'simple_image':
        allowed_background_modes = ['color', 'system_image', 'upload_image']
    elif active_template in {'simple_pattern', 'simple_retro'}:
        allowed_background_modes = ['color', 'gradient', 'pattern']

    requested_section = str(request.GET.get('section') or 'naslovi').strip()
    active_section = requested_section if requested_section in {'naslovi', 'pozadine'} else 'naslovi'
    if active_section == 'pozadine' and not supports_background_editor:
        active_section = 'naslovi'

    if request.method == 'POST':
        if 'save_title_settings' in request.POST or request.POST.get('reset_titles_mode') == 'all':
            reset_mode = request.POST.get('reset_titles_mode')

            if reset_mode == 'all':
                for field_name in title_fields:
                    if field_name in default_active_design:
                        current_design[field_name] = str(default_active_design[field_name])
                messages.success(request, 'Naslovi su vraćeni na default.')
            else:
                for field_name in title_fields:
                    if field_name in request.POST:
                        current_design[field_name] = request.POST.get(field_name)
                messages.success(request, 'Promjene naslova i datuma su spremljene.')

            design_customizations[active_template] = current_design
            set_blog_preferences(request.user, {
                'design_customizations': design_customizations,
            })
            return redirect(reverse('design_live_editor_titles') + '?section=naslovi')

        if 'save_background_settings' in request.POST or request.POST.get('reset_background_mode') == 'all' or request.POST.get('delete_simple_background_image') == '1' or request.FILES.get('simple_background_image'):
            if not supports_background_editor:
                messages.warning(request, 'Pozadine su trenutno dostupne samo za simple dizajne.')
                return redirect(reverse('design_live_editor_titles') + '?section=naslovi')

            reset_mode = request.POST.get('reset_background_mode')
            if reset_mode == 'all':
                for field_name in background_fields:
                    if field_name in default_active_design_raw:
                        current_design[field_name] = default_active_design_raw[field_name]

                if profile.simple_background_image:
                    profile.simple_background_image.delete(save=False)
                    profile.simple_background_image = None
                    profile.save(update_fields=['simple_background_image'])

                messages.success(request, 'Pozadine su vraćene na default.')
            else:
                for field_name in background_fields:
                    if field_name in request.POST:
                        current_design[field_name] = request.POST.get(field_name)

                selected_mode = str(current_design.get('outer_background_mode') or '').strip()
                if selected_mode not in allowed_background_modes and allowed_background_modes:
                    current_design['outer_background_mode'] = allowed_background_modes[0]
                    selected_mode = allowed_background_modes[0]

                if active_template in {'simple_pattern', 'simple_retro'}:
                    current_design['header_background_mode'] = 'color'
                    header_color = str(request.POST.get('header_background_color_1') or current_design.get('header_background_color_1') or default_active_design_raw.get('header_background_color_1') or '#d98a37').strip()
                    current_design['header_background_color_1'] = header_color
                    current_design['header_background_color_2'] = header_color

                if request.POST.get('delete_simple_background_image') == '1' and profile.simple_background_image:
                    profile.simple_background_image.delete(save=False)
                    profile.simple_background_image = None

                if request.FILES.get('simple_background_image'):
                    image_error = validate_design_background_upload(request.FILES['simple_background_image'])
                    if image_error:
                        messages.error(request, image_error)
                        return redirect(reverse('design_live_editor_titles') + '?section=pozadine')

                    if profile.simple_background_image and profile.simple_background_image.name:
                        profile.simple_background_image.delete(save=False)
                    profile.simple_background_image = request.FILES['simple_background_image']
                    current_design['outer_background_mode'] = 'upload_image'

                profile.save()
                messages.success(request, 'Promjene pozadina su spremljene.')

            design_customizations[active_template] = current_design
            set_blog_preferences(request.user, {
                'design_customizations': design_customizations,
            })
            return redirect(reverse('design_live_editor_titles') + '?section=pozadine')

    active_design_customization = build_design_customization_payload(current_design)

    context = {
        'profile': profile,
        'design_font_choices': get_design_font_choices(),
        'design_template_labels': DESIGN_TEMPLATE_LABELS,
        'active_design_template': active_template,
        'active_design_customization': active_design_customization,
        'default_active_design_customization': default_active_design,
        'preview_url': reverse('profile') + '?live_editor_preview=1',
        'full_preview_url': reverse('profile'),
        'live_editor_section': active_section,
        'supports_background_editor': supports_background_editor,
        'background_mode_choices': [
            {'value': value, 'label': DESIGN_BACKGROUND_MODE_LABELS[value]}
            for value in allowed_background_modes
        ],
        'design_pattern_choices': get_design_pattern_choices(),
        'design_background_image_choices': get_design_background_image_choices(),
        'design_gradient_direction_choices': get_design_gradient_direction_choices(),
        'post_date_style_choices': POST_DATE_STYLE_CHOICES,
        'post_date_effect_choices': POST_DATE_EFFECT_CHOICES,
        'current_simple_background_url': profile.simple_background_image.url if profile.simple_background_image else '',
    }
    return render(request, 'blog/design_live_editor.html', context)
