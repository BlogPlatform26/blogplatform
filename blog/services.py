import base64
import calendar
import io
import json
import math
import os
import random
import re
import unicodedata
from urllib.parse import urlencode
from collections import deque
from datetime import datetime, time
from statistics import median

from django.utils import timezone
from django.shortcuts import render
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count, F, Q
from django.db.models.functions import Coalesce, TruncMonth
from django.urls import reverse
from django.utils.safestring import mark_safe

try:
    from PIL import Image
except Exception:
    Image = None

from .analytics import build_live_analytics_context, build_tracking_context
from .constants import CATEGORY_FOLDER_MAP, MONTHS_HR
from .forms import CommentForm
from .music_library import get_ambient_music_track
from .models import (
    Category,
    CategoryHomeImage,
    Follow,
    PollVote,
    Post,
    QuizAnswer,
    Tag,
    UserBlock,
    UserRestriction,
    UserBox,
    SpecialDayEvent,
    SpecialDayMessage,
    SpecialDaySelection,
    AuthorQuestion,
    HomeFeaturedPost,
)


ANONYMOUS_COMMENT_USERNAME = "__anon_comment_user__"
COMMENT_SETTINGS_FILE = os.path.join(settings.BASE_DIR, 'blog', 'comment_settings.json')
BLOG_PREFERENCES_FILE = os.path.join(settings.BASE_DIR, 'blog', 'blog_preferences.json')


def resolve_design_template_name(template_key):
    template_aliases = {
        'soho': 'studio',
    }
    resolved_template = template_aliases.get(template_key, template_key or 'default')
    return f'blog/designs/{resolved_template}.html'

DEFAULT_DESIGN_FONT_CHOICES = [
    ('system', 'System'),
    ('arial', 'Arial'),
    ('georgia', 'Georgia'),
    ('verdana', 'Verdana'),
    ('trebuchet', 'Trebuchet MS'),
    ('times', 'Times New Roman'),
    ('garamond', 'Garamond'),
    ('palatino', 'Palatino'),
    ('helvetica', 'Helvetica'),
    ('tahoma', 'Tahoma'),
]

DESIGN_FONT_STACKS = {
    'system': '-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif',
    'arial': 'Arial, Helvetica, sans-serif',
    'georgia': 'Georgia, Times New Roman, serif',
    'verdana': 'Verdana, Geneva, sans-serif',
    'trebuchet': 'Trebuchet MS, Helvetica, sans-serif',
    'times': 'Times New Roman, Times, serif',
    'garamond': 'Garamond, Georgia, serif',
    'palatino': 'Palatino Linotype, Palatino, serif',
    'helvetica': 'Helvetica, Arial, sans-serif',
    'tahoma': 'Tahoma, Geneva, sans-serif',
}

DESIGN_PATTERN_CHOICES = [
    ('paper', 'Papir'),
    ('dots', 'Točkice'),
    ('grid', 'Mreža'),
    ('hearts', 'Srca'),
    ('flowers', 'Cvijeće'),
    ('pencils', 'Olovke'),
    ('paws', 'Životinje / šapice'),
    ('stars', 'Zvjezdice'),
    ('music', 'Note / glazba'),
    ('butterflies', 'Leptiri'),
    ('books', 'Knjige'),
    ('clouds', 'Oblaci'),
    ('bows', 'Mašne'),
]

DESIGN_PATTERN_ASSETS = {
    'paper': 'blog/images/design-backgrounds/paper_pattern.png',
    'dots': 'blog/images/design-backgrounds/dots_pattern.png',
    'grid': 'blog/images/design-backgrounds/grid.png',
    'hearts': 'blog/images/design-backgrounds/pattern-hearts.svg',
    'flowers': 'blog/images/design-backgrounds/pattern-flowers.svg',
    'pencils': 'blog/images/design-backgrounds/pattern-pencils.svg',
    'paws': 'blog/images/design-backgrounds/pattern-paws.svg',
    'stars': 'blog/images/design-backgrounds/pattern-stars.svg',
    'music': 'blog/images/design-backgrounds/pattern-music.svg',
    'butterflies': 'blog/images/design-backgrounds/pattern-butterflies.svg',
    'books': 'blog/images/design-backgrounds/pattern-books.svg',
    'clouds': 'blog/images/design-backgrounds/pattern-clouds.svg',
    'bows': 'blog/images/design-backgrounds/pattern-bows.svg',
}

DESIGN_BACKGROUND_IMAGE_CHOICES = [
    ('bookshelf', 'Police s knjigama'),
    ('cute_pets_flower', 'Pas i mačka'),
    ('abstract_earth', 'Apstraktni tonovi'),
    ('blue_tech', 'Plava tehnologija'),
    ('dreamy_sunset', 'Zamagljeni zalazak'),
    ('misty_mountains', 'Maglovite planine'),
    ('night_camp', 'Noćno kampiranje'),
    ('navy_coffee', 'Kava i bilježnica'),
    ('watercolor_workspace', 'Kreativni stol'),
    ('soho_sunrise', 'Planinsko jutro'),
    ('soho_sunrise_valley', 'Svitanje u dolini'),
    ('soho_meadow_light', 'Sunčana livada'),
    ('soho_morning_peaks', 'Jutarnji vrhovi'),
    ('cozy_workspace_breakfast', 'Ugodan stol uz kavu'),
    ('happy_dog_living_room', 'Veseli pas u dnevnom boravku'),
    ('sweet_brunch_table', 'Slatki stol'),
    ('romantic_roses_evening', 'Romantične ruže'),
    ('poetry_and_roses', 'Poezija i cvijeće'),
    ('ruzicasti_vrt', 'Ružičasti vrt'),
    ('stara_aleja', 'Stara aleja'),
    ('staza_prema_vrhovima', 'Staza prema vrhovima'),
    ('jedro_u_suton', 'Jedro u suton'),
    ('misticno_jezero', 'Mistična laguna'),
    ('cozy_cat_morning', 'Mačka kraj prozora'),
    ('sunset_beach', 'Zalazak na plaži'),
    ('podvodna_tisina', 'Podvodna tišina'),
    ('vodopad_u_magli', 'Vodopad u magli'),
    ('planine_u_magli', 'Planine u magli'),
    ('nebeski_mir', 'Nebeski mir'),
    ('iznad_oblaka', 'Iznad oblaka'),
    ('sumska_svjetlost', 'Šumska svjetlost'),
    ('polarna_svjetlost', 'Polarna svjetlost'),
    ('zlatno_polje', 'Zlatno polje'),
    ('neonski_grad', 'Neonski grad'),
    ('polje_lavande', 'Polje lavande'),
    ('carobna_ljubicasta', 'Čarobni sumrak'),
    ('kraljevska_pozornica', 'Kraljevska pozornica'),
    ('dimni_akordi', 'Dimni akordi'),
    ('sjene_ulice', 'Sjene ulice'),
    ('mjesecev_ples', 'Mjesečev ples'),
]

DESIGN_BACKGROUND_IMAGE_ASSETS = {
    'bookshelf': 'blog/images/design-backgrounds/bookshelf.png',
    'cute_pets_flower': 'blog/images/design-backgrounds/cute_pets_flower.png',
    'abstract_earth': 'blog/images/design-backgrounds/abstract_earth.png',
    'blue_tech': 'blog/images/design-backgrounds/blue_tech.png',
    'dreamy_sunset': 'blog/images/design-backgrounds/dreamy_sunset.png',
    'misty_mountains': 'blog/images/design-backgrounds/misty_mountains.png',
    'night_camp': 'blog/images/design-backgrounds/night_camp.png',
    'navy_coffee': 'blog/images/design-backgrounds/navy_coffee.png',
    'watercolor_workspace': 'blog/images/design-backgrounds/watercolor_workspace.png',
    'soho_sunrise': 'blog/images/design-backgrounds/soho_sunrise.jpg',
    'soho_sunrise_valley': 'blog/images/design-backgrounds/soho_sunrise_valley.jpg',
    'soho_meadow_light': 'blog/images/design-backgrounds/soho_meadow_light.jpg',
    'soho_morning_peaks': 'blog/images/design-backgrounds/soho_morning_peaks.jpg',
    'cozy_workspace_breakfast': 'blog/images/design-backgrounds/cozy_workspace_breakfast.png',
    'happy_dog_living_room': 'blog/images/design-backgrounds/happy_dog_living_room.png',
    'sweet_brunch_table': 'blog/images/design-backgrounds/sweet_brunch_table.png',
    'romantic_roses_evening': 'blog/images/design-backgrounds/romantic_roses_evening.png',
    'poetry_and_roses': 'blog/images/design-backgrounds/poetry_and_roses.png',
    'ruzicasti_vrt': 'blog/images/design-backgrounds/ruzicasti_vrt.jpg',
    'stara_aleja': 'blog/images/design-backgrounds/stara_aleja.jpg',
    'staza_prema_vrhovima': 'blog/images/design-backgrounds/staza_prema_vrhovima.png',
    'jedro_u_suton': 'blog/images/design-backgrounds/jedro_u_suton.png',
    'misticno_jezero': 'blog/images/design-backgrounds/misticno_jezero.jpg',
    'cozy_cat_morning': 'blog/images/design-backgrounds/cozy_cat_morning.png',
    'sunset_beach': 'blog/images/design-backgrounds/sunset_beach.png',
    'litica_noci': 'blog/images/design-backgrounds/litica_noci.png',
    'podvodna_tisina': 'blog/images/design-backgrounds/podvodna_tisina.png',
    'vodopad_u_magli': 'blog/images/design-backgrounds/vodopad_u_magli.png',
    'planine_u_magli': 'blog/images/design-backgrounds/planine_u_magli.jpg',
    'nebeski_mir': 'blog/images/design-backgrounds/nebeski_mir.jpg',
    'iznad_oblaka': 'blog/images/design-backgrounds/iznad_oblaka.jpg',
    'sumska_svjetlost': 'blog/images/design-backgrounds/sumska_svjetlost.jpg',
    'polarna_svjetlost': 'blog/images/design-backgrounds/polarna_svjetlost.jpg',
    'zlatno_polje': 'blog/images/design-backgrounds/zlatno_polje.jpg',
    'neonski_grad': 'blog/images/design-backgrounds/neonski_grad.jpg',
    'polje_lavande': 'blog/images/design-backgrounds/polje_lavande.jpg',
    'carobna_ljubicasta': 'blog/images/design-backgrounds/carobna_ljubicasta.jpg',
    'kraljevska_pozornica': 'blog/images/design-backgrounds/kraljevska_pozornica.jpg',
    'dimni_akordi': 'blog/images/design-backgrounds/dimni_akordi.png',
    'sjene_ulice': 'blog/images/design-backgrounds/sjene_ulice.png',
    'mjesecev_ples': 'blog/images/design-backgrounds/mjesecev_ples.png',
}


SOHO_COVER_IMAGE_CHOICES = [
    ('soho_sunrise', 'Studio naslovna slika'),
]

SOHO_COVER_IMAGE_ASSETS = {
    'soho_sunrise': 'blog/images/design-backgrounds/soho_sunrise.jpg',
}

ALL_DESIGN_BACKGROUND_IMAGE_ASSETS = {
    **DESIGN_BACKGROUND_IMAGE_ASSETS,
    **SOHO_COVER_IMAGE_ASSETS,
}

DESIGN_BACKGROUND_MODES = {
    'color',
    'gradient',
    'pattern',
    'system_image',
    'upload_image',
}

DESIGN_GRADIENT_DIRECTIONS = {
    'to bottom',
    'to right',
    '135deg',
}

RIGHT_LAYOUT_DESIGN_TEMPLATES = {
    'default_right',
    'dark_right',
    'classic_right',
}

POST_DATE_STYLE_OPTIONS = {
    'classic_vertical',
    'slim_vertical',
    'card',
    'minimal_inline',
    'split',
    'ribbon',
    'boxed_number',
    'corner_tag',
    'soft',
    'newspaper',
}

POST_DATE_EFFECT_OPTIONS = {
    'solid',
    'duo',
    'gradient',
}

DEFAULT_DESIGN_CUSTOMIZATIONS = {
    'default': {
        'blog_title_font': 'georgia',
        'blog_title_color': '#3f3128',
        'post_title_font': 'georgia',
        'post_title_color': '#111827',
        'box_title_font': 'georgia',
        'box_title_color': '#3f3128',
        'post_date_color': '#7a2cff',
        'body_font': 'arial',
        'body_text_color': '#2f241c',
        'right_box_columns': '1',
    },
    'dark': {
        'blog_title_font': 'georgia',
        'blog_title_color': '#ffffff',
        'post_title_font': 'georgia',
        'post_title_color': '#ffffff',
        'box_title_font': 'georgia',
        'box_title_color': '#ffffff',
        'post_date_color': '#ff3b3b',
        'body_font': 'arial',
        'body_text_color': '#f3f4f6',
        'right_box_columns': '1',
    },
    'classic': {
        'blog_title_font': 'georgia',
        'blog_title_color': '#111111',
        'post_title_font': 'georgia',
        'post_title_color': '#1f1f1f',
        'box_title_font': 'georgia',
        'box_title_color': '#111111',
        'post_date_color': '#7a2cff',
        'body_font': 'georgia',
        'body_text_color': '#3a3028',
        'right_box_columns': '1',
    },
    'default_right': {
        'blog_title_font': 'georgia',
        'blog_title_color': '#3f3128',
        'post_title_font': 'georgia',
        'post_title_color': '#111827',
        'box_title_font': 'georgia',
        'box_title_color': '#3f3128',
        'post_date_color': '#7a2cff',
        'body_font': 'arial',
        'body_text_color': '#2f241c',
        'right_box_columns': '2',
    },
    'dark_right': {
        'blog_title_font': 'georgia',
        'blog_title_color': '#ffffff',
        'post_title_font': 'georgia',
        'post_title_color': '#ffffff',
        'box_title_font': 'georgia',
        'box_title_color': '#ffffff',
        'post_date_color': '#ff3b3b',
        'body_font': 'arial',
        'body_text_color': '#f3f4f6',
        'right_box_columns': '2',
    },
    'classic_right': {
        'blog_title_font': 'georgia',
        'blog_title_color': '#111111',
        'post_title_font': 'georgia',
        'post_title_color': '#1f1f1f',
        'box_title_font': 'georgia',
        'box_title_color': '#111111',
        'post_date_color': '#7a2cff',
        'body_font': 'georgia',
        'body_text_color': '#3a3028',
        'right_box_columns': '2',
    },
    'simple_pattern': {
        'blog_title_font': 'georgia',
        'blog_title_color': '#ffffff',
        'post_title_font': 'georgia',
        'post_title_color': '#3f7f93',
        'box_title_font': 'arial',
        'box_title_color': '#4c5961',
        'post_date_color': '#c97d27',
        'body_font': 'arial',
        'body_text_color': '#57534e',
        'outer_background_mode': 'pattern',
        'outer_background_color_1': '#efe4c9',
        'outer_background_color_2': '#e1d0ac',
        'outer_background_pattern': 'paper',
        'outer_background_image': 'soft_light',
        'outer_background_gradient_direction': 'to bottom',
        'header_background_mode': 'gradient',
        'header_background_color_1': '#d98a37',
        'header_background_color_2': '#b8641e',
        'header_background_gradient_direction': 'to bottom',
        'content_background_color': '#fffefb',
        'content_border_color': '#d9c8ad',
        'box_background_color': '#fffefb',
        'box_border_color': '#ddd5c9',
        'right_box_columns': '1',
    },
    'simple_image': {
        'blog_title_font': 'georgia',
        'blog_title_color': '#ffffff',
        'post_title_font': 'georgia',
        'post_title_color': '#3f7f93',
        'box_title_font': 'arial',
        'box_title_color': '#4c5961',
        'post_date_color': '#c97d27',
        'body_font': 'arial',
        'body_text_color': '#57534e',
        'outer_background_mode': 'system_image',
        'outer_background_color_1': '#f5efe6',
        'outer_background_color_2': '#e8dccf',
        'outer_background_pattern': 'paper',
        'outer_background_image': 'bookshelf',
        'outer_background_gradient_direction': 'to bottom',
        'header_background_mode': 'color',
        'header_background_color_1': '#c8b16b',
        'header_background_color_2': '#a38a4a',
        'header_background_gradient_direction': 'to right',
        'content_background_color': '#fffefb',
        'content_border_color': '#d9c8ad',
        'box_background_color': '#fffefb',
        'box_border_color': '#ddd5c9',
        'right_box_columns': '1',
    },
    'simple_retro': {
        'blog_title_font': 'arial',
        'blog_title_color': '#4a9aa6',
        'post_title_font': 'arial',
        'post_title_color': '#4a9aa6',
        'box_title_font': 'arial',
        'box_title_color': '#5a5146',
        'post_date_color': '#7b8b8e',
        'body_font': 'arial',
        'body_text_color': '#5c564d',
        'outer_background_mode': 'color',
        'outer_background_color_1': '#f1efe7',
        'outer_background_color_2': '#e5dece',
        'outer_background_pattern': 'paper',
        'outer_background_image': 'soft_light',
        'outer_background_gradient_direction': 'to bottom',
        'header_background_mode': 'gradient',
        'header_background_color_1': '#d8dccf',
        'header_background_color_2': '#c5cab7',
        'header_background_gradient_direction': 'to bottom',
        'content_background_color': '#fbfaf6',
        'content_border_color': '#d7d1c4',
        'box_background_color': '#fbfaf6',
        'box_border_color': '#d7d1c4',
        'right_box_columns': '1',
    },
    'soho': {
        'blog_title_font': 'georgia',
        'blog_title_color': '#2f241c',
        'post_title_font': 'georgia',
        'post_title_color': '#2f241c',
        'box_title_font': 'georgia',
        'box_title_color': '#44382d',
        'post_date_color': '#b67a2d',
        'body_font': 'arial',
        'body_text_color': '#4b4137',
        'outer_background_mode': 'system_image',
        'outer_background_color_1': '#ece7df',
        'outer_background_color_2': '#ece7df',
        'outer_background_pattern': 'paper',
        'outer_background_image': 'soho_sunrise',
        'outer_background_gradient_direction': 'to bottom',
        'header_background_mode': 'color',
        'header_background_color_1': '#ece7df',
        'header_background_color_2': '#ece7df',
        'header_background_gradient_direction': 'to right',
        'content_background_color': '#fbf8f3',
        'content_border_color': '#ddd3c7',
        'box_background_color': '#d9d2c8',
        'box_border_color': '#d9d2c8',
        'right_box_columns': '1',
    },
    'magazin': {
        'blog_title_font': 'georgia',
        'blog_title_color': '#ffffff',
        'post_title_font': 'georgia',
        'post_title_color': '#4f4136',
        'box_title_font': 'garamond',
        'box_title_color': '#54463b',
        'post_date_color': '#9b7b5a',
        'body_font': 'arial',
        'body_text_color': '#5e5043',
        'outer_background_mode': 'system_image',
        'outer_background_color_1': '#dce9e3',
        'outer_background_color_2': '#dce9e3',
        'outer_background_pattern': 'paper',
        'outer_background_image': 'soho_sunrise_valley',
        'outer_background_gradient_direction': 'to bottom',
        'header_background_mode': 'color',
        'header_background_color_1': '#f6f1ea',
        'header_background_color_2': '#f6f1ea',
        'header_background_gradient_direction': 'to right',
        'content_background_color': '#fffaf5',
        'content_border_color': '#ddd1c4',
        'box_background_color': '#f8f3ed',
        'box_border_color': '#e6dbcf',
        'right_box_columns': '1',
    },
    'litica_noci': {
        'blog_title_font': 'georgia',
        'blog_title_color': '#f3f8ff',
        'post_title_font': 'georgia',
        'post_title_color': '#f3f8ff',
        'box_title_font': 'georgia',
        'box_title_color': '#d6e6ff',
        'post_date_color': '#95acd6',
        'body_font': 'arial',
        'body_text_color': '#d7e4ff',
        'outer_background_mode': 'system_image',
        'outer_background_color_1': '#000000',
        'outer_background_color_2': '#000000',
        'outer_background_pattern': 'paper',
        'outer_background_image': 'litica_noci',
        'outer_background_gradient_direction': 'to bottom',
        'header_background_mode': 'color',
        'header_background_color_1': '#000000',
        'header_background_color_2': '#000000',
        'header_background_gradient_direction': 'to right',
        'content_background_color': 'transparent',
        'content_border_color': 'rgba(203, 220, 255, 0.24)',
        'box_background_color': 'transparent',
        'box_border_color': 'rgba(203, 220, 255, 0.24)',
        'right_box_columns': '1',
    },
    'podvodna_tisina': {
        'blog_title_font': 'georgia',
        'blog_title_color': '#f1f6ff',
        'post_title_font': 'georgia',
        'post_title_color': '#eef5ff',
        'box_title_font': 'georgia',
        'box_title_color': '#cfe1ff',
        'post_date_color': '#88b6ff',
        'body_font': 'arial',
        'body_text_color': '#d5e5ff',
        'outer_background_mode': 'system_image',
        'outer_background_color_1': '#010611',
        'outer_background_color_2': '#010611',
        'outer_background_pattern': 'paper',
        'outer_background_image': 'podvodna_tisina',
        'outer_background_gradient_direction': 'to bottom',
        'header_background_mode': 'color',
        'header_background_color_1': '#010611',
        'header_background_color_2': '#010611',
        'header_background_gradient_direction': 'to right',
        'content_background_color': 'transparent',
        'content_border_color': 'rgba(197, 220, 255, 0.22)',
        'box_background_color': 'transparent',
        'box_border_color': 'rgba(197, 220, 255, 0.22)',
        'right_box_columns': '1',
    },
    'vodopad_u_magli': {
        'blog_title_font': 'georgia',
        'blog_title_color': '#425146',
        'post_title_font': 'georgia',
        'post_title_color': '#475649',
        'box_title_font': 'garamond',
        'box_title_color': '#607060',
        'post_date_color': '#789180',
        'body_font': 'arial',
        'body_text_color': '#5f675d',
        'outer_background_mode': 'system_image',
        'outer_background_color_1': '#f2f1ed',
        'outer_background_color_2': '#f2f1ed',
        'outer_background_pattern': 'paper',
        'outer_background_image': 'vodopad_u_magli',
        'outer_background_gradient_direction': 'to bottom',
        'header_background_mode': 'color',
        'header_background_color_1': '#f2f1ed',
        'header_background_color_2': '#f2f1ed',
        'header_background_gradient_direction': 'to right',
        'content_background_color': 'transparent',
        'content_border_color': 'rgba(137, 151, 138, 0.34)',
        'box_background_color': 'transparent',
        'box_border_color': 'rgba(137, 151, 138, 0.34)',
        'right_box_columns': '1',
    },
    'planine_u_magli': {
        'blog_title_font': 'georgia',
        'blog_title_color': '#5b6877',
        'post_title_font': 'georgia',
        'post_title_color': '#617181',
        'box_title_font': 'garamond',
        'box_title_color': '#6c7d8f',
        'post_date_color': '#8ea3bb',
        'body_font': 'arial',
        'body_text_color': '#5f6975',
        'outer_background_mode': 'system_image',
        'outer_background_color_1': '#f6f5f2',
        'outer_background_color_2': '#f6f5f2',
        'outer_background_pattern': 'paper',
        'outer_background_image': 'planine_u_magli',
        'outer_background_gradient_direction': 'to bottom',
        'header_background_mode': 'color',
        'header_background_color_1': '#f6f5f2',
        'header_background_color_2': '#f6f5f2',
        'header_background_gradient_direction': 'to right',
        'content_background_color': 'transparent',
        'content_border_color': 'rgba(160, 175, 196, 0.30)',
        'box_background_color': 'transparent',
        'box_border_color': 'rgba(160, 175, 196, 0.30)',
        'right_box_columns': '1',
    },

'iznad_oblaka': {
    'blog_title_font': 'georgia',
    'blog_title_color': '#f7eff7',
    'post_title_font': 'georgia',
    'post_title_color': '#fff4fb',
    'box_title_font': 'garamond',
    'box_title_color': '#f0dbe9',
    'post_date_color': '#f4c9d9',
    'body_font': 'arial',
    'body_text_color': '#eadce8',
    'outer_background_mode': 'system_image',
    'outer_background_color_1': '#000000',
    'outer_background_color_2': '#000000',
    'outer_background_pattern': 'paper',
    'outer_background_image': 'iznad_oblaka',
    'outer_background_gradient_direction': 'to bottom',
    'header_background_mode': 'color',
    'header_background_color_1': '#000000',
    'header_background_color_2': '#000000',
    'header_background_gradient_direction': 'to right',
    'content_background_color': 'transparent',
    'content_border_color': 'rgba(245, 220, 235, 0.22)',
    'box_background_color': 'transparent',
    'box_border_color': 'rgba(245, 220, 235, 0.22)',
    'right_box_columns': '1',
},
'sumska_svjetlost': {
    'blog_title_font': 'georgia',
    'blog_title_color': '#56614d',
    'post_title_font': 'georgia',
    'post_title_color': '#53604b',
    'box_title_font': 'garamond',
    'box_title_color': '#66755b',
    'post_date_color': '#7ea06c',
    'body_font': 'arial',
    'body_text_color': '#5d6957',
    'outer_background_mode': 'system_image',
    'outer_background_color_1': '#e7f1df',
    'outer_background_color_2': '#e7f1df',
    'outer_background_pattern': 'paper',
    'outer_background_image': 'sumska_svjetlost',
    'outer_background_gradient_direction': 'to bottom',
    'header_background_mode': 'color',
    'header_background_color_1': '#e7f1df',
    'header_background_color_2': '#e7f1df',
    'header_background_gradient_direction': 'to right',
    'content_background_color': 'transparent',
    'content_border_color': 'rgba(136, 162, 116, 0.24)',
    'box_background_color': 'transparent',
    'box_border_color': 'rgba(136, 162, 116, 0.24)',
    'right_box_columns': '1',
},
'polarna_svjetlost': {
    'blog_title_font': 'georgia',
    'blog_title_color': '#e9f8ff',
    'post_title_font': 'georgia',
    'post_title_color': '#edf8ff',
    'box_title_font': 'garamond',
    'box_title_color': '#d6efff',
    'post_date_color': '#bdefff',
    'body_font': 'arial',
    'body_text_color': '#def1ff',
    'outer_background_mode': 'system_image',
    'outer_background_color_1': '#5d85ab',
    'outer_background_color_2': '#5d85ab',
    'outer_background_pattern': 'paper',
    'outer_background_image': 'polarna_svjetlost',
    'outer_background_gradient_direction': 'to bottom',
    'header_background_mode': 'color',
    'header_background_color_1': '#5d85ab',
    'header_background_color_2': '#5d85ab',
    'header_background_gradient_direction': 'to right',
    'content_background_color': 'transparent',
    'content_border_color': 'rgba(173, 225, 245, 0.24)',
    'box_background_color': 'transparent',
    'box_border_color': 'rgba(173, 225, 245, 0.24)',
    'right_box_columns': '1',
},
'zlatno_polje': {
    'blog_title_font': 'georgia',
    'blog_title_color': '#5a3605',
    'post_title_font': 'georgia',
    'post_title_color': '#4b2d05',
    'box_title_font': 'garamond',
    'box_title_color': '#6c4410',
    'post_date_color': '#8a6119',
    'body_font': 'arial',
    'body_text_color': '#5f3d10',
    'outer_background_mode': 'system_image',
    'outer_background_color_1': '#d9a63a',
    'outer_background_color_2': '#d9a63a',
    'outer_background_pattern': 'paper',
    'outer_background_image': 'zlatno_polje',
    'outer_background_gradient_direction': 'to bottom',
    'header_background_mode': 'color',
    'header_background_color_1': '#d9a63a',
    'header_background_color_2': '#d9a63a',
    'header_background_gradient_direction': 'to right',
    'content_background_color': 'transparent',
    'content_border_color': 'rgba(146, 92, 17, 0.22)',
    'box_background_color': 'transparent',
    'box_border_color': 'rgba(146, 92, 17, 0.22)',
    'right_box_columns': '1',
},
'neonski_grad': {
    'blog_title_font': 'system',
    'blog_title_color': '#f6efff',
    'post_title_font': 'system',
    'post_title_color': '#f9f4ff',
    'box_title_font': 'system',
    'box_title_color': '#f0e5ff',
    'post_date_color': '#7ee8ff',
    'body_font': 'system',
    'body_text_color': '#eedfff',
    'outer_background_mode': 'system_image',
    'outer_background_color_1': '#18082f',
    'outer_background_color_2': '#18082f',
    'outer_background_pattern': 'paper',
    'outer_background_image': 'neonski_grad',
    'outer_background_gradient_direction': 'to bottom',
    'header_background_mode': 'color',
    'header_background_color_1': '#18082f',
    'header_background_color_2': '#18082f',
    'header_background_gradient_direction': 'to right',
    'content_background_color': 'transparent',
    'content_border_color': 'rgba(131, 103, 255, 0.24)',
    'box_background_color': 'transparent',
    'box_border_color': 'rgba(131, 103, 255, 0.24)',
    'right_box_columns': '1',
},
'polje_lavande': {
    'blog_title_font': 'georgia',
    'blog_title_color': '#4f2768',
    'post_title_font': 'georgia',
    'post_title_color': '#4a235f',
    'box_title_font': 'garamond',
    'box_title_color': '#6a3c84',
    'post_date_color': '#8d5bc0',
    'body_font': 'arial',
    'body_text_color': '#5a3271',
    'outer_background_mode': 'system_image',
    'outer_background_color_1': '#d9b0ee',
    'outer_background_color_2': '#d9b0ee',
    'outer_background_pattern': 'paper',
    'outer_background_image': 'polje_lavande',
    'outer_background_gradient_direction': 'to bottom',
    'header_background_mode': 'color',
    'header_background_color_1': '#d9b0ee',
    'header_background_color_2': '#d9b0ee',
    'header_background_gradient_direction': 'to right',
    'content_background_color': 'transparent',
    'content_border_color': 'rgba(255, 255, 255, 0.22)',
    'box_background_color': 'transparent',
    'box_border_color': 'rgba(255, 255, 255, 0.22)',
    'right_box_columns': '1',
},
'carobna_ljubicasta': {
    'blog_title_font': 'georgia',
    'blog_title_color': '#fff3ff',
    'post_title_font': 'georgia',
    'post_title_color': '#fff1ff',
    'box_title_font': 'garamond',
    'box_title_color': '#f8efff',
    'post_date_color': '#ffd0ff',
    'body_font': 'arial',
    'body_text_color': '#f6eeff',
    'outer_background_mode': 'system_image',
    'outer_background_color_1': '#542b7e',
    'outer_background_color_2': '#542b7e',
    'outer_background_pattern': 'paper',
    'outer_background_image': 'carobna_ljubicasta',
    'outer_background_gradient_direction': 'to bottom',
    'header_background_mode': 'color',
    'header_background_color_1': '#542b7e',
    'header_background_color_2': '#542b7e',
    'header_background_gradient_direction': 'to right',
    'content_background_color': 'rgba(33, 12, 56, 0.12)',
    'content_border_color': 'rgba(255, 255, 255, 0.10)',
    'box_background_color': 'rgba(33, 12, 56, 0.12)',
    'box_border_color': 'rgba(255, 255, 255, 0.10)',
    'right_box_columns': '1',
},
'kraljevska_pozornica': {
    'blog_title_font': 'georgia',
    'blog_title_color': '#fff0e1',
    'post_title_font': 'georgia',
    'post_title_color': '#fff4e8',
    'box_title_font': 'garamond',
    'box_title_color': '#ffd7af',
    'post_date_color': '#ffbe7a',
    'body_font': 'arial',
    'body_text_color': '#f4ddd1',
    'outer_background_mode': 'system_image',
    'outer_background_color_1': '#16070b',
    'outer_background_color_2': '#16070b',
    'outer_background_pattern': 'paper',
    'outer_background_image': 'kraljevska_pozornica',
    'outer_background_gradient_direction': 'to bottom',
    'header_background_mode': 'color',
    'header_background_color_1': '#21090f',
    'header_background_color_2': '#21090f',
    'header_background_gradient_direction': 'to right',
    'content_background_color': 'rgba(24, 8, 12, 0.38)',
    'content_border_color': 'rgba(255, 201, 142, 0.16)',
    'box_background_color': 'rgba(24, 8, 12, 0.34)',
    'box_border_color': 'rgba(255, 201, 142, 0.14)',
    'right_box_columns': '1',
},

'nebeska_klasika': {
    'blog_title_font': 'georgia',
    'blog_title_color': '#514d57',
    'post_title_font': 'georgia',
    'post_title_color': '#534842',
    'box_title_font': 'georgia',
    'box_title_color': '#584d46',
    'post_date_color': '#7f7468',
    'body_font': 'arial',
    'body_text_color': '#4b463f',
    'outer_background_mode': 'system_image',
    'outer_background_color_1': '#ece7dc',
    'outer_background_color_2': '#ece7dc',
    'outer_background_pattern': 'paper',
    'outer_background_image': 'soft_light',
    'outer_background_gradient_direction': 'to bottom',
    'header_background_mode': 'color',
    'header_background_color_1': '#ece7dc',
    'header_background_color_2': '#ece7dc',
    'header_background_gradient_direction': 'to right',
    'content_background_color': '#faf7f0',
    'content_border_color': '#c0b4a4',
    'box_background_color': '#faf7f0',
    'box_border_color': '#c0b4a4',
    'right_box_columns': '1',
},
'ponocna_elegancija': {
    'blog_title_font': 'georgia',
    'blog_title_color': '#f2f4fb',
    'post_title_font': 'georgia',
    'post_title_color': '#f2f5fb',
    'box_title_font': 'georgia',
    'box_title_color': '#f3f5fb',
    'post_date_color': '#b8c2d8',
    'body_font': 'arial',
    'body_text_color': '#d8dde8',
    'outer_background_mode': 'system_image',
    'outer_background_color_1': '#05070d',
    'outer_background_color_2': '#05070d',
    'outer_background_pattern': 'paper',
    'outer_background_image': 'litica_noci',
    'outer_background_gradient_direction': 'to bottom',
    'header_background_mode': 'color',
    'header_background_color_1': '#05070d',
    'header_background_color_2': '#05070d',
    'header_background_gradient_direction': 'to right',
    'content_background_color': '#070c16',
    'content_border_color': '#aab8dc',
    'box_background_color': '#070c16',
    'box_border_color': '#aab8dc',
    'right_box_columns': '1',
},
'ruzicasti_vrt': {
    'blog_title_font': 'georgia',
    'blog_title_color': '#6b5056',
    'post_title_font': 'georgia',
    'post_title_color': '#6b5056',
    'box_title_font': 'georgia',
    'box_title_color': '#6b5056',
    'post_date_color': '#9f8283',
    'body_font': 'arial',
    'body_text_color': '#5e4b4f',
    'outer_background_mode': 'system_image',
    'outer_background_color_1': '#f6d8dd',
    'outer_background_color_2': '#f6d8dd',
    'outer_background_pattern': 'paper',
    'outer_background_image': 'ruzicasti_vrt',
    'outer_background_gradient_direction': 'to bottom',
    'header_background_mode': 'color',
    'header_background_color_1': '#f6d8dd',
    'header_background_color_2': '#f6d8dd',
    'header_background_gradient_direction': 'to right',
    'content_background_color': '#fff9f7',
    'content_border_color': '#ffffff',
    'box_background_color': '#fff9f7',
    'box_border_color': '#ffffff',
    'right_box_columns': '1',
},
'stara_aleja': {
    'blog_title_font': 'georgia',
    'blog_title_color': '#5d4738',
    'post_title_font': 'georgia',
    'post_title_color': '#5a4335',
    'box_title_font': 'georgia',
    'box_title_color': '#6a503e',
    'post_date_color': '#8e7460',
    'body_font': 'arial',
    'body_text_color': '#53463c',
    'outer_background_mode': 'system_image',
    'outer_background_color_1': '#eadbc6',
    'outer_background_color_2': '#eadbc6',
    'outer_background_pattern': 'paper',
    'outer_background_image': 'stara_aleja',
    'outer_background_gradient_direction': 'to bottom',
    'header_background_mode': 'color',
    'header_background_color_1': '#eadbc6',
    'header_background_color_2': '#eadbc6',
    'header_background_gradient_direction': 'to right',
    'content_background_color': '#fbf3e7',
    'content_border_color': '#c2a07f',
    'box_background_color': '#fbf3e7',
    'box_border_color': '#c2a07f',
    'right_box_columns': '1',
},
'staza_prema_vrhovima': {
    'blog_title_font': 'georgia',
    'blog_title_color': '#fff3df',
    'post_title_font': 'georgia',
    'post_title_color': '#fff1dc',
    'box_title_font': 'georgia',
    'box_title_color': '#ffe1ae',
    'post_date_color': '#e5bc7d',
    'body_font': 'arial',
    'body_text_color': '#f2e3ce',
    'outer_background_mode': 'system_image',
    'outer_background_color_1': '#2f2419',
    'outer_background_color_2': '#2f2419',
    'outer_background_pattern': 'paper',
    'outer_background_image': 'staza_prema_vrhovima',
    'outer_background_gradient_direction': 'to bottom',
    'header_background_mode': 'color',
    'header_background_color_1': '#2f2419',
    'header_background_color_2': '#2f2419',
    'header_background_gradient_direction': 'to right',
    'content_background_color': 'rgba(51, 35, 22, 0.58)',
    'content_border_color': 'rgba(255, 224, 176, 0.22)',
    'box_background_color': 'rgba(49, 34, 22, 0.52)',
    'box_border_color': 'rgba(255, 224, 176, 0.18)',
    'right_box_columns': '1',
},
'jedro_u_suton': {
    'blog_title_font': 'georgia',
    'blog_title_color': '#fff7ee',
    'post_title_font': 'georgia',
    'post_title_color': '#fff7ef',
    'box_title_font': 'georgia',
    'box_title_color': '#fff5ea',
    'post_date_color': '#f6d0ae',
    'body_font': 'arial',
    'body_text_color': '#fbefe3',
    'outer_background_mode': 'system_image',
    'outer_background_color_1': '#2d1f18',
    'outer_background_color_2': '#2d1f18',
    'outer_background_pattern': 'paper',
    'outer_background_image': 'jedro_u_suton',
    'outer_background_gradient_direction': 'to bottom',
    'header_background_mode': 'color',
    'header_background_color_1': '#2d1f18',
    'header_background_color_2': '#2d1f18',
    'header_background_gradient_direction': 'to right',
    'content_background_color': 'rgba(58, 34, 24, 0.12)',
    'content_border_color': 'rgba(255, 232, 208, 0.10)',
    'box_background_color': 'rgba(58, 34, 24, 0.10)',
    'box_border_color': 'rgba(255, 232, 208, 0.10)',
    'right_box_columns': '1',
},
'misticno_jezero': {
    'blog_title_font': 'georgia',
    'blog_title_color': '#fff4ff',
    'post_title_font': 'georgia',
    'post_title_color': '#fff3ff',
    'box_title_font': 'georgia',
    'box_title_color': '#ffe9c7',
    'post_date_color': '#f7c88f',
    'body_font': 'arial',
    'body_text_color': '#f5e9ff',
    'outer_background_mode': 'system_image',
    'outer_background_color_1': '#22112f',
    'outer_background_color_2': '#22112f',
    'outer_background_pattern': 'paper',
    'outer_background_image': 'misticno_jezero',
    'outer_background_gradient_direction': 'to bottom',
    'header_background_mode': 'color',
    'header_background_color_1': '#22112f',
    'header_background_color_2': '#22112f',
    'header_background_gradient_direction': 'to right',
    'content_background_color': 'rgba(42, 18, 62, 0.36)',
    'content_border_color': 'rgba(255, 234, 199, 0.18)',
    'box_background_color': 'rgba(35, 14, 52, 0.32)',
    'box_border_color': 'rgba(255, 234, 199, 0.16)',
    'right_box_columns': '1',
},
'svemirski_horizont': {
    'blog_title_font': 'georgia',
    'blog_title_color': '#eff6ff',
    'post_title_font': 'georgia',
    'post_title_color': '#eff6ff',
    'box_title_font': 'garamond',
    'box_title_color': '#dcecff',
    'post_date_color': '#9cc8ff',
    'body_font': 'arial',
    'body_text_color': '#d9e8ff',
    'outer_background_mode': 'system_image',
    'outer_background_color_1': '#020611',
    'outer_background_color_2': '#020611',
    'outer_background_pattern': 'paper',
    'outer_background_image': 'litica_noci',
    'outer_background_gradient_direction': 'to bottom',
    'header_background_mode': 'color',
    'header_background_color_1': '#020611',
    'header_background_color_2': '#020611',
    'header_background_gradient_direction': 'to right',
    'content_background_color': '#06101a',
    'content_border_color': '#9cc8ff',
    'box_background_color': '#06101a',
    'box_border_color': '#9cc8ff',
    'right_box_columns': '1',
},
'zlatni_horizont': {
    'blog_title_font': 'georgia',
    'blog_title_color': '#fff0db',
    'post_title_font': 'georgia',
    'post_title_color': '#ffe7c4',
    'box_title_font': 'garamond',
    'box_title_color': '#ffd39a',
    'post_date_color': '#ffbf72',
    'body_font': 'arial',
    'body_text_color': '#f5dfc6',
    'outer_background_mode': 'system_image',
    'outer_background_color_1': '#140b08',
    'outer_background_color_2': '#140b08',
    'outer_background_pattern': 'paper',
    'outer_background_image': 'kraljevska_pozornica',
    'outer_background_gradient_direction': 'to bottom',
    'header_background_mode': 'color',
    'header_background_color_1': '#140b08',
    'header_background_color_2': '#140b08',
    'header_background_gradient_direction': 'to right',
    'content_background_color': '#1b110d',
    'content_border_color': '#ffbf72',
    'box_background_color': '#1b110d',
    'box_border_color': '#ffbf72',
    'right_box_columns': '1',
},
'nebeski_mir': {

        'blog_title_font': 'georgia',
        'blog_title_color': '#81879a',
        'post_title_font': 'georgia',
        'post_title_color': '#6f7588',
        'box_title_font': 'garamond',
        'box_title_color': '#8f96aa',
        'post_date_color': '#97a381',
        'body_font': 'arial',
        'body_text_color': '#72788a',
        'outer_background_mode': 'system_image',
        'outer_background_color_1': '#f5f1f7',
        'outer_background_color_2': '#f5f1f7',
        'outer_background_pattern': 'paper',
        'outer_background_image': 'nebeski_mir',
        'outer_background_gradient_direction': 'to bottom',
        'header_background_mode': 'color',
        'header_background_color_1': '#f5f1f7',
        'header_background_color_2': '#f5f1f7',
        'header_background_gradient_direction': 'to right',
        'content_background_color': 'transparent',
        'content_border_color': 'rgba(201, 191, 215, 0.34)',
        'box_background_color': 'transparent',
        'box_border_color': 'rgba(201, 191, 215, 0.34)',
        'right_box_columns': '1',
    },

    'sjene_ulice': {
    'blog_title_font': 'georgia',
    'blog_title_color': '#f6eee6',
    'post_title_font': 'georgia',
    'post_title_color': '#f7efe7',
    'box_title_font': 'georgia',
    'box_title_color': '#f4e7d8',
    'post_date_color': '#c9b2a0',
    'body_font': 'arial',
    'body_text_color': '#efe2d4',
    'outer_background_mode': 'system_image',
    'outer_background_color_1': '#14100e',
    'outer_background_color_2': '#14100e',
    'outer_background_pattern': 'paper',
    'outer_background_image': 'sjene_ulice',
    'outer_background_gradient_direction': 'to bottom',
    'header_background_mode': 'color',
    'header_background_color_1': '#14100e',
    'header_background_color_2': '#14100e',
    'header_background_gradient_direction': 'to right',
    'content_background_color': 'rgba(19, 15, 13, 0.48)',
    'content_border_color': 'rgba(247, 211, 172, 0.10)',
    'box_background_color': 'rgba(19, 15, 13, 0.48)',
    'box_border_color': 'rgba(247, 211, 172, 0.10)',
    'right_box_columns': '1',
},
'mjesecev_ples': {
    'blog_title_font': 'georgia',
    'blog_title_color': '#f1e6d4',
    'post_title_font': 'georgia',
    'post_title_color': '#f5ebdd',
    'box_title_font': 'georgia',
    'box_title_color': '#e8d5b3',
    'post_date_color': '#c9b07f',
    'body_font': 'arial',
    'body_text_color': '#e7dccd',
    'outer_background_mode': 'gradient',
    'outer_background_color_1': '#0c0b09',
    'outer_background_color_2': '#3e3328',
    'outer_background_gradient_direction': 'to bottom',
    'header_background_mode': 'gradient',
    'header_background_color_1': '#16120f',
    'header_background_color_2': '#574535',
    'header_background_gradient_direction': 'to right',
    'content_background_color': 'rgba(18, 15, 13, 0.40)',
    'content_border_color': 'rgba(210, 186, 146, 0.14)',
    'box_background_color': 'rgba(18, 15, 13, 0.34)',
    'box_border_color': 'rgba(210, 186, 146, 0.10)',
    'right_box_columns': '1',
},
'asfaltni_plamen': {
    'blog_title_font': 'georgia',
    'blog_title_color': '#f4e7d8',
    'post_title_font': 'georgia',
    'post_title_color': '#f8eee3',
    'box_title_font': 'georgia',
    'box_title_color': '#e5b77d',
    'post_date_color': '#dca060',
    'body_font': 'arial',
    'body_text_color': '#efe1d2',
    'outer_background_mode': 'gradient',
    'outer_background_color_1': '#0d0a08',
    'outer_background_color_2': '#4d2e1f',
    'outer_background_gradient_direction': 'to bottom',
    'header_background_mode': 'gradient',
    'header_background_color_1': '#1a120e',
    'header_background_color_2': '#7a4321',
    'header_background_gradient_direction': 'to right',
    'content_background_color': 'rgba(24, 17, 13, 0.20)',
    'content_border_color': 'rgba(221, 160, 101, 0.14)',
    'box_background_color': 'rgba(24, 17, 13, 0.20)',
    'box_border_color': 'rgba(221, 160, 101, 0.10)',
    'right_box_columns': '1',
},
'dimni_akordi': {
        'blog_title_font': 'georgia',
        'blog_title_color': '#f6dfc0',
        'post_title_font': 'georgia',
        'post_title_color': '#f8e8d3',
        'box_title_font': 'georgia',
        'box_title_color': '#efc48e',
        'post_date_color': '#d39a5e',
        'body_font': 'arial',
        'body_text_color': '#f1ddc8',
        'outer_background_mode': 'gradient',
        'outer_background_color_1': '#120b09',
        'outer_background_color_2': '#6d3b1e',
        'outer_background_gradient_direction': '135deg',
        'header_background_mode': 'gradient',
        'header_background_color_1': '#3a1d12',
        'header_background_color_2': '#a65a23',
        'header_background_gradient_direction': 'to right',
        'content_background_color': 'rgba(34, 18, 12, 0.58)',
        'content_border_color': 'rgba(214, 145, 84, 0.24)',
        'box_background_color': 'rgba(34, 18, 12, 0.50)',
        'box_border_color': 'rgba(214, 145, 84, 0.18)',
        'right_box_columns': '1',
    },
}

def _get_default_post_date_style(template_name):
    if template_name in {'default', 'default_right'}:
        return 'classic_vertical'
    if template_name in {'dark', 'dark_right'}:
        return 'newspaper'
    if template_name in {'classic', 'classic_right'}:
        return 'split'
    if template_name in {'simple_pattern', 'simple_image'}:
        return 'card'
    if template_name == 'simple_retro':
        return 'minimal_inline'
    if template_name in {'soho', 'magazin'}:
        return 'boxed_number'
    return 'classic_vertical'


def _get_default_post_date_effect(template_name):
    if template_name in {'default', 'default_right'}:
        return 'gradient'
    if template_name in {'classic', 'classic_right', 'simple_pattern', 'simple_image', 'simple_retro'}:
        return 'duo'
    return 'solid'


def _get_default_post_date_secondary_color(template_name, primary_color):
    secondary_map = {
        'default': '#ffd200',
        'default_right': '#ffd200',
        'classic': '#d4a84f',
        'classic_right': '#d4a84f',
        'dark': '#f8d6d6',
        'dark_right': '#f8d6d6',
        'simple_pattern': '#7a8a92',
        'simple_image': '#7a8a92',
        'simple_retro': '#6f7f86',
        'soho': '#7f8c8d',
        'magazin': '#ffd200',
    }
    return secondary_map.get(template_name, primary_color or '#ffd200')


def _apply_default_post_date_settings():
    for template_name, values in DEFAULT_DESIGN_CUSTOMIZATIONS.items():
        primary_color = str(values.get('post_date_color') or '#d97706')
        values.setdefault('post_date_style', _get_default_post_date_style(template_name))
        values.setdefault('post_date_effect', _get_default_post_date_effect(template_name))
        values.setdefault('post_date_color_1', primary_color)
        values.setdefault('post_date_color_2', _get_default_post_date_secondary_color(template_name, primary_color))
        values.setdefault('post_date_size', '100')


_apply_default_post_date_settings()


DEFAULT_AMBIENT_MUSIC_TRACK = 'music_for_video-forest-lullaby-110624'


DEFAULT_BLOG_PREFERENCES = {
    'cursor_style': 'default',
    'cursor_effect': 'none',
    'ambient_music_enabled': False,
    'ambient_music_track': '',
    'ambient_music_volume': 18,
    'posts_per_page': 5,
    'show_post_tags': True,
    'show_post_comments': True,
    'allow_comments': True,
    'blog_archive_mode': 'both',
    'analytics_live_counter_enabled': False,
    'analytics_map_enabled': False,
    'analytics_geo_enabled': False,
    'analytics_active_pages_enabled': False,
    'analytics_widget_side': 'right_top',
    'analytics_map_variant': 'map',
    'analytics_stat_card_size': 'small',
    'design_customizations': DEFAULT_DESIGN_CUSTOMIZATIONS,
}





def _cursor_preview_markup(svg):
    return mark_safe(svg.strip())


BLOG_CURSOR_CHOICES = (
    {
        'value': 'default',
        'label': 'Obični kursor (default)',
        'description': 'Standardni obični kursor bez posebnog stila.',
        'preview_html': _cursor_preview_markup('<svg class="ambience-svg-preview ambience-svg-preview--default" viewBox="0 0 64 64" aria-hidden="true"><path d="M16 10L50 31L35 35L42 53L34 56L27 38L16 49Z" fill="#4b5563" stroke="#111827" stroke-width="3" stroke-linejoin="round"/><path d="M16 10L30 41" fill="none" stroke="#9ca3af" stroke-width="2.5" stroke-linecap="round"/></svg>'),
    },
    {
        'value': 'sparkle',
        'label': 'Zvjezdani',
        'description': 'Ljubičasta zvjezdica sa sjajem.',
        'preview_html': _cursor_preview_markup('<svg class="ambience-svg-preview ambience-svg-preview--sparkle" viewBox="0 0 64 64" aria-hidden="true"><path d="M32 9l5.5 15.5L53 30l-15.5 5.5L32 51l-5.5-15.5L11 30l15.5-5.5Z" fill="#8b5cf6" stroke="#5b21b6" stroke-width="3" stroke-linejoin="round"/><circle cx="50" cy="49" r="6" fill="#ddd6fe" stroke="#7c3aed" stroke-width="2.2"/></svg>'),
    },
    {
        'value': 'heart',
        'label': 'Srce',
        'description': 'Nježni ružičasti kursor u obliku srca.',
        'preview_html': _cursor_preview_markup('<svg class="ambience-svg-preview ambience-svg-preview--heart" viewBox="0 0 64 64" aria-hidden="true"><path d="M32 54S13 43 8 28c-4-10 2-20 12-20 5 0 9 2 12 7 3-5 7-7 12-7 10 0 16 10 12 20-5 15-24 26-24 26Z" fill="#fb7185" stroke="#be123c" stroke-width="3" stroke-linejoin="round"/></svg>'),
    },
    {
        'value': 'moon',
        'label': 'Mjesec',
        'description': 'Plavi polumjesec za mirniji izgled.',
        'preview_html': _cursor_preview_markup('<svg class="ambience-svg-preview ambience-svg-preview--moon" viewBox="0 0 64 64" aria-hidden="true"><path d="M41 10c-2 15 7 28 17 32-4 7-12 12-22 12-14 0-25-11-25-25 0-10 6-19 15-23 2 1 9 4 15 4Z" fill="#60a5fa" stroke="#1d4ed8" stroke-width="3" stroke-linejoin="round"/><circle cx="45" cy="18" r="4" fill="#bfdbfe"/></svg>'),
    },
    {
        'value': 'diamond',
        'label': 'Dijamant',
        'description': 'Zlatni sjajni dijamant.',
        'preview_html': _cursor_preview_markup('<svg class="ambience-svg-preview ambience-svg-preview--diamond" viewBox="0 0 64 64" aria-hidden="true"><path d="M21 10h22l13 15-24 29L8 25z" fill="#fbbf24" stroke="#b45309" stroke-width="3" stroke-linejoin="round"/><path d="M21 10l11 15 11-15M8 25h48M32 25v29" fill="none" stroke="#fef3c7" stroke-width="2.2" stroke-linejoin="round"/></svg>'),
    },
    {
        'value': 'neon',
        'label': 'Neon',
        'description': 'Tirkizni moderni neon stil.',
        'preview_html': _cursor_preview_markup('<svg class="ambience-svg-preview ambience-svg-preview--neon" viewBox="0 0 64 64" aria-hidden="true"><path d="M12 9l36 21-15 3 8 18-7 3-8-18-12 11Z" fill="#22d3ee" stroke="#0f172a" stroke-width="3" stroke-linejoin="round"/><path d="M12 9l20 25" fill="none" stroke="#a5f3fc" stroke-width="2.4" stroke-linecap="round"/></svg>'),
    },
    {
        'value': 'rose',
        'label': 'Ruža',
        'description': 'Ruža sa stabljikom, ne obični cvijet.',
        'preview_html': _cursor_preview_markup('<svg class="ambience-svg-preview ambience-svg-preview--rose" viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M32 11c3-3 8-2 11 1 3 3 3 8 0 11 2 4 1 9-2 12-4 4-10 4-14 1-4 3-10 2-14-2-3-3-4-8-2-12-3-3-3-8 0-11 3-3 8-4 11-1 2-2 7-2 10 1Z" fill="#ec4899" stroke="#9d174d" stroke-width="2.8"/><path d="M32 15c2-2 5-2 7 0 2 2 2 5 0 7 2 2 2 5 0 7s-5 2-7 0c-2 2-5 2-7 0s-2-5 0-7c-2-2-2-5 0-7 2-2 5-2 7 0Z" fill="#f9a8d4" stroke="#be185d" stroke-width="2.1"/><path d="M32 36v18" stroke="#15803d" stroke-width="3.2"/><path d="M31 41c-7 0-11 3-13 9 5 1 10-1 13-5M33 45c4-5 9-6 15-4-2 6-6 9-13 9" fill="#86efac" stroke="#4d7c0f" stroke-width="2"/></g></svg>'),
    },
    {
        'value': 'butterfly',
        'label': 'Leptir',
        'description': 'Nježni leptir u ljubičasto-ružičastim tonovima.',
        'preview_html': _cursor_preview_markup('<svg class="ambience-svg-preview ambience-svg-preview--butterfly" viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M31 27c-5-10-16-12-21-4-4 7 1 18 15 18M33 27c5-10 16-12 21-4 4 7-1 18-15 18" fill="#c084fc" stroke="#7c3aed" stroke-width="2.8"/><path d="M31 34c-4 9-13 11-17 5-3-5 1-12 11-12M33 34c4 9 13 11 17 5 3-5-1-12-11-12" fill="#f9a8d4" stroke="#be185d" stroke-width="2.4"/><path d="M32 20v24" stroke="#374151" stroke-width="2.8"/><path d="M32 20l-4-6M32 20l4-6" stroke="#374151" stroke-width="2.2"/></g></svg>'),
    },
    {
        'value': 'leaf',
        'label': 'List',
        'description': 'Zeleni prirodni stil s listom.',
        'preview_html': _cursor_preview_markup('<svg class="ambience-svg-preview ambience-svg-preview--leaf" viewBox="0 0 64 64" aria-hidden="true"><path d="M52 13c-20 0-34 11-39 28-3 10 4 16 13 16 18 0 32-15 33-44-2 0-4 0-7 0Z" fill="#4ade80" stroke="#166534" stroke-width="3" stroke-linejoin="round"/><path d="M18 46c10-10 18-15 31-23M28 36c-2 5-2 10-1 14" fill="none" stroke="#14532d" stroke-width="2.4" stroke-linecap="round"/></svg>'),
    },
    {
        'value': 'sun',
        'label': 'Sunce',
        'description': 'Topli sunčani kursor sa zrakama.',
        'preview_html': _cursor_preview_markup('<svg class="ambience-svg-preview ambience-svg-preview--sun" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="12" fill="#fbbf24" stroke="#d97706" stroke-width="3"/><path d="M32 7v10M32 47v10M7 32h10M47 32h10M14 14l7 7M43 43l7 7M14 50l7-7M43 21l7-7" fill="none" stroke="#f59e0b" stroke-width="3" stroke-linecap="round"/></svg>'),
    },

    {
        'value': 'flame',
        'label': 'Plamen',
        'description': 'Vatreni kursor u obliku plamena.',
        'preview_html': _cursor_preview_markup('<svg class="ambience-svg-preview ambience-svg-preview--flame" viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M33 8c4 6 5 11 2 15-2 3-5 5-7 8-3 3-5 7-5 12 0 9 7 16 16 16s16-7 16-17c0-9-6-14-11-20-1 3-3 6-6 8 1-3 1-7-1-12Z" fill="#f97316" stroke="#c2410c" stroke-width="3"/><path d="M33 22c2 3 3 5 2 8-1 2-3 3-4 5-2 2-3 4-3 7 0 6 4 10 10 10s10-4 10-11c0-5-3-9-7-13-1 2-2 4-4 5 1-2 0-5-1-11Z" fill="#fde68a" stroke="#f59e0b" stroke-width="2.3"/></g></svg>'),
    },
    {
        'value': 'crown',
        'label': 'Kruna',
        'description': 'Mala zlatna kruna kao kursor.',
        'preview_html': _cursor_preview_markup('<svg class="ambience-svg-preview ambience-svg-preview--crown" viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke-linejoin="round"><path d="M12 46l5-24 15 12 15-12 5 24Z" fill="#fbbf24" stroke="#a16207" stroke-width="3"/><path d="M17 22l10 8 5-14 5 14 10-8" fill="none" stroke="#fde68a" stroke-width="2.4"/><path d="M15 46h34" stroke="#78350f" stroke-width="3.2" stroke-linecap="round"/><circle cx="17" cy="21" r="3" fill="#fef3c7" stroke="#a16207" stroke-width="2"/><circle cx="32" cy="15" r="3" fill="#fca5a5" stroke="#b91c1c" stroke-width="2"/><circle cx="47" cy="21" r="3" fill="#bfdbfe" stroke="#1d4ed8" stroke-width="2"/></g></svg>'),
    },
    {
        'value': 'crystal',
        'label': 'Kristal',
        'description': 'Ljubičasto-plavi kristal sa sjajem.',
        'preview_html': _cursor_preview_markup('<svg class="ambience-svg-preview ambience-svg-preview--crystal" viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke-linejoin="round"><path d="M24 9h16l11 14-19 32L13 23Z" fill="#a78bfa" stroke="#5b21b6" stroke-width="3"/><path d="M24 9l8 14 8-14M13 23h38M32 23v32" fill="none" stroke="#ddd6fe" stroke-width="2.4"/><path d="M28 36l4 5 5-8" fill="none" stroke="#e0f2fe" stroke-width="2.4" stroke-linecap="round"/></g></svg>'),
    },
    {
        'value': 'paw',
        'label': 'Šapica',
        'description': 'Slatka šapica u tamnijim tonovima.',
        'preview_html': _cursor_preview_markup('<svg class="ambience-svg-preview ambience-svg-preview--paw" viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="20" cy="20" rx="6" ry="8" fill="#fda4af" stroke="#9f1239" stroke-width="2.6"/><ellipse cx="31" cy="15" rx="6" ry="8" fill="#fda4af" stroke="#9f1239" stroke-width="2.6"/><ellipse cx="43" cy="18" rx="6" ry="8" fill="#fda4af" stroke="#9f1239" stroke-width="2.6"/><ellipse cx="50" cy="30" rx="6" ry="8" fill="#fda4af" stroke="#9f1239" stroke-width="2.6"/><path d="M17 40c0-9 7-15 15-15 10 0 18 7 18 17 0 8-7 14-17 14-9 0-16-6-16-16Z" fill="#fb7185" stroke="#881337" stroke-width="3"/></g></svg>'),
    },
    {
        'value': 'droplet',
        'label': 'Kapljica',
        'description': 'Plava kapljica vode.',
        'preview_html': _cursor_preview_markup('<svg class="ambience-svg-preview ambience-svg-preview--droplet" viewBox="0 0 64 64" aria-hidden="true"><path d="M32 8c8 12 17 20 17 31 0 10-8 18-17 18S15 49 15 39c0-11 9-19 17-31Z" fill="#38bdf8" stroke="#0369a1" stroke-width="3" stroke-linejoin="round"/><path d="M27 43c2 2 4 3 7 3 5 0 9-3 10-8" fill="none" stroke="#e0f2fe" stroke-width="2.6" stroke-linecap="round"/></svg>'),
    },
    {
        'value': 'sword',
        'label': 'Munja',
        'description': 'Oštar kursor u obliku žute munje.',
        'preview_html': _cursor_preview_markup('<svg class="ambience-svg-preview ambience-svg-preview--lightning" viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke-linejoin="round" stroke-linecap="round"><path d="M36 7 16 33h14l-4 24 22-30H34Z" fill="#fde047" stroke="#ca8a04" stroke-width="3.2"/><path d="M35 13 24 28h11l-2 12 10-15h-9Z" fill="#fff7ae" stroke="#facc15" stroke-width="2.1"/></g></svg>'),
    },
    {
        'value': 'skeleton_hand',
        'label': 'Komet',
        'description': 'Mali komet sa svijetlim tragom.',
        'preview_html': _cursor_preview_markup('<svg class="ambience-svg-preview ambience-svg-preview--comet" viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M10 40c12-1 22-8 29-20" stroke="#c4b5fd" stroke-width="6"/><path d="M8 47c13-1 26-9 34-24" stroke="#e9d5ff" stroke-width="3.4"/><circle cx="44" cy="18" r="10" fill="#38bdf8" stroke="#1d4ed8" stroke-width="3"/><path d="M41 15l3 2 4-5" stroke="#e0f2fe" stroke-width="2.4"/></g></svg>'),
    },
)


IMPORTED_CURSOR_CHOICES = (
    {
        'value': 'imported_spajalica',
        'label': 'Spajalica',
        'description': 'Metalna spajalica kao kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/spajalica.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAB90lEQVR4nN3XMWgTURzH8e9fOsQQ0MHJjg5OIq4OxsEO1qVDFDodiFMWFzuHzHYSabdCHATJIoJ1EMWIg95hrUMEwdBbFD1dBIPS5edwr/GuJJqjdxfwD1nuhfv8Xt7l3f8ZxVYFOALUEtd+Ad+BHwBWIH4UOAtcAOaBqrv+GXgIvAC+FYkvAfc0poBXQIP0L5M7ftdhA+DnmBDrwPyhAvDzwBVJy2a2DRyWVMnZmYgv8Wfmb4CPE5bgNTkvQRZ8G7gKHPsv8AqwANyZBQ7x7K85ICgbh/ghWgA2gEHZOO6mHtCbJe47bHcW+NY+dDfxPHil4okQT4DlWeFBVnwuI34JuC7pTLvdHg20Wi3M7C1wG3hMhtfstP1ACl+9uYoMQKzcWNnDbwEPsuDTBkjha+trmAwhms3mgfBpAqTwTqczGvA878D4vwKk8G63675tXG40csH/FiCFP9rcBAMBixcXc8MnBUjhvV5vNFCv13PFx1Xqfx4EgQLfl+/7pWyvNeI2KZCkfr8ff971S8EBTuAaizAMFe7sKAzD0vAa8Rb6QZK+RpGiKCoNh3j2G5I0HA6Te/tW0fgccV930oWgWq1iZgPgJXAfeEaBR6i9AMclnTOz58QnmaeAD3zCHSKLKnMBTgOnHPge+FI0vL8qxB1uKUeoZP0GGmsHjkarRZYAAAAASUVORK5CYII=') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAB90lEQVR4nN3XMWgTURzH8e9fOsQQ0MHJjg5OIq4OxsEO1qVDFDodiFMWFzuHzHYSabdCHATJIoJ1EMWIg95hrUMEwdBbFD1dBIPS5edwr/GuJJqjdxfwD1nuhfv8Xt7l3f8ZxVYFOALUEtd+Ad+BHwBWIH4UOAtcAOaBqrv+GXgIvAC+FYkvAfc0poBXQIP0L5M7ftdhA+DnmBDrwPyhAvDzwBVJy2a2DRyWVMnZmYgv8Wfmb4CPE5bgNTkvQRZ8G7gKHPsv8AqwANyZBQ7x7K85ICgbh/ghWgA2gEHZOO6mHtCbJe47bHcW+NY+dDfxPHil4okQT4DlWeFBVnwuI34JuC7pTLvdHg20Wi3M7C1wG3hMhtfstP1ACl+9uYoMQKzcWNnDbwEPsuDTBkjha+trmAwhms3mgfBpAqTwTqczGvA878D4vwKk8G63675tXG40csH/FiCFP9rcBAMBixcXc8MnBUjhvV5vNFCv13PFx1Xqfx4EgQLfl+/7pWyvNeI2KZCkfr8ff971S8EBTuAaizAMFe7sKAzD0vAa8Rb6QZK+RpGiKCoNh3j2G5I0HA6Te/tW0fgccV930oWgWq1iZgPgJXAfeEaBR6i9AMclnTOz58QnmaeAD3zCHSKLKnMBTgOnHPge+FI0vL8qxB1uKUeoZP0GGmsHjkarRZYAAAAASUVORK5CYII=') 2 2, pointer",
    },
    {
        'value': 'imported_plava_strelica',
        'label': 'Plava strelica',
        'description': 'Plava strelica kao kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/plava_strelica.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAADoUlEQVR4nMXXz2ucRRzH8ffM8+xuknXdJNtsSpDSk5QeLEYEEc968uBZQVFBi6YJDaX1IlLwJjZWECsxSkE96Ek8VRREKCkF/SfUNrvN/uj+fJ758fWwz6LtszVLk60DA8szMJ8XM888O18FcHjLLwBzQB7IMWgR0AHqN1/VVSbU1OEtXwQWgXKCyCZjMVAHKpNE6CQwn4QvAo8kfTF5VgbmklWaCCCX9CyQDy88vdHdfGkjQU0coe9+ECwd4+j6ZcyvXz4QRArQaBuOH9csvfAy/StbE0ekAOI9R7LCoWOK0nOv0P7+0kQRaYATfusIb5ehcFRReOY1mt9enBgiDUDRui2cyEFhUZErK2aeepPG1x9MBJEGCMQdz2YDXlxQZAqaYE4x/eQK9a/eP3BECoD3+K7jagMUkMsqMlOaoCTklk9Ru3z+QBEjABBHHtOEb24JYagIw4BgKiScF7LLK9S+eOfAEOkt0IKNPCbyRC2FiYEA9FRAkM8QFh2Z5XV2t84eCCIF8M5hohhjhH4PbARiB9sRTOcIilPohw2Zx0+zu3V634gRWyC4yGIceAvWgPMgXoHWBMUZwkMP4QsR+sQZqpur+0KMOIYWawwu9oNwC94PRlBAqNGlPMHSLKZkCZ44R+XSqftGpADKemJj6RswDpwTEBA1QIiAKE1QKqCPlDElTbB8lsqnK/eFSAGceEzfE3khjgTrwHqFNQpjFKansB2FaWuEHGp+FrswQ/DYGSqfvHUvRHFsAOIxXogt9ARiAzYWTCxEHU/UMERNS1yzcMtA06FMiJ0uoh9dp/LRybsRef655KRamMpHIBLakWfaC9IH2/K4Tg9bq5GxgA4IgwAIwHrEgfgAkVlU6Xl2zj+7sfjulbUkeHjfGA/gnQcLs6Gi0QVagm8YXLVOqXKN2o0fIa6BVoOXUvzgLXUxOA22h+r/ea+8vQEA4jTVpkK1FNQM0mgzv3ONeneb8upna2PO3WFwr4ySPi5AwGpoBVAVZLfP3M429dZVyq9/uJZMXB8DMLzUDiHjAcQL0tdwE6Tap1C9TqPxE+U3LgzDd5KJ7R6Af1/rm2MDEA+9ANox05XrtG//QPlkKrwCdMcAxP8VPhrgQDqebP13+s3vKK9cHBV+YHXCiBUwyF+/YPvblFc/nmj4SIDu/oG98TmL7/088XAYlGYL3FkN5ZOxiYfDYAVi7jxaD7Q2VPA/V8fDH8k/1vDbPQTseYz22/4GrvgB8OktBhwAAAAASUVORK5CYII=') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAADoUlEQVR4nMXXz2ucRRzH8ffM8+xuknXdJNtsSpDSk5QeLEYEEc968uBZQVFBi6YJDaX1IlLwJjZWECsxSkE96Ek8VRREKCkF/SfUNrvN/uj+fJ758fWwz6LtszVLk60DA8szMJ8XM888O18FcHjLLwBzQB7IMWgR0AHqN1/VVSbU1OEtXwQWgXKCyCZjMVAHKpNE6CQwn4QvAo8kfTF5VgbmklWaCCCX9CyQDy88vdHdfGkjQU0coe9+ECwd4+j6ZcyvXz4QRArQaBuOH9csvfAy/StbE0ekAOI9R7LCoWOK0nOv0P7+0kQRaYATfusIb5ehcFRReOY1mt9enBgiDUDRui2cyEFhUZErK2aeepPG1x9MBJEGCMQdz2YDXlxQZAqaYE4x/eQK9a/eP3BECoD3+K7jagMUkMsqMlOaoCTklk9Ru3z+QBEjABBHHtOEb24JYagIw4BgKiScF7LLK9S+eOfAEOkt0IKNPCbyRC2FiYEA9FRAkM8QFh2Z5XV2t84eCCIF8M5hohhjhH4PbARiB9sRTOcIilPohw2Zx0+zu3V634gRWyC4yGIceAvWgPMgXoHWBMUZwkMP4QsR+sQZqpur+0KMOIYWawwu9oNwC94PRlBAqNGlPMHSLKZkCZ44R+XSqftGpADKemJj6RswDpwTEBA1QIiAKE1QKqCPlDElTbB8lsqnK/eFSAGceEzfE3khjgTrwHqFNQpjFKansB2FaWuEHGp+FrswQ/DYGSqfvHUvRHFsAOIxXogt9ARiAzYWTCxEHU/UMERNS1yzcMtA06FMiJ0uoh9dp/LRybsRef655KRamMpHIBLakWfaC9IH2/K4Tg9bq5GxgA4IgwAIwHrEgfgAkVlU6Xl2zj+7sfjulbUkeHjfGA/gnQcLs6Gi0QVagm8YXLVOqXKN2o0fIa6BVoOXUvzgLXUxOA22h+r/ea+8vQEA4jTVpkK1FNQM0mgzv3ONeneb8upna2PO3WFwr4ySPi5AwGpoBVAVZLfP3M429dZVyq9/uJZMXB8DMLzUDiHjAcQL0tdwE6Tap1C9TqPxE+U3LgzDd5KJ7R6Af1/rm2MDEA+9ANox05XrtG//QPlkKrwCdMcAxP8VPhrgQDqebP13+s3vKK9cHBV+YHXCiBUwyF+/YPvblFc/nmj4SIDu/oG98TmL7/088XAYlGYL3FkN5ZOxiYfDYAVi7jxaD7Q2VPA/V8fDH8k/1vDbPQTseYz22/4GrvgB8OktBhwAAAAASUVORK5CYII=') 2 2, pointer",
    },
    {
        'value': 'imported_duga',
        'label': 'Duga',
        'description': 'Šarena duga kao kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/duga.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAE+klEQVR4nL2XTWgbVxSFP4UXeAMJzIADGpDBU1LomG4k6MIGL6qu4tBFbdJFDF1EECgxXTShi2C8KCKLELxI8wNt3UCLuinWJsSLlqoLg7IIyAUHTRfBY0hhDA7MgwrmQQami5Esjfwb8nM3o7l6uue8c89cvQFgc6OZNBu1JAw2E95x5FqPV5KV76+hdYidd3E/Ok/5s6sYhpF7FwSEDsMUfKxE+G+bxm9VtA6JojAxDOutkxDpRVIxishCEd1RVP+ooZWivf5nMl785K2SONH7YIYgNZjCpFqYpb3RoH5vnubqnbfqDbFfUsaS6sg0nghY/mUBZ61O4LcS2ym9cTVO7J/WcDrAdRVXpmy8p01qSxWaq3eS6L/wjaqxPwGpoeCDaOOYmuoFB601Kw8WqN2/QhS+ORJ7WyA0jAYgVTcRYUq4esnE27GoPaizrBWtRi0pTl0kdzL3Wm0ZIqDBDsD0gai/wpHIMU3xLDiuQ/WbBr7XIlQBycskeR0SWQIyhBEfCAfALSiQ5gSYZsStezbeVkTt3i20Dl/LoH0PCA2jCoTqg492wUXYpypAC9AfGkwuGTQe3mV5qUL7yaMkil7dG30Ctp+VXhpQMLPggAY8GdGSEd5IhPuTRaQClpcq1O9fIdwJXolEv/SIR6bvo2ZqxCGX+AJaElQ3r2SE9TOgbZoX64ThNmGwmVj2e8dqyUALBk1nQUGz64VuKMAbAN+N2EZ3ZjFv1vD+blL7YZ7geftYSmTnQK/vY9AzXS804AtjiBKAhVbTRC8qoGcwbz7Ce7JK7XaF5u8/JsnL6FAiWQLSSvu+B9zCE1ZG+v6XNlHnPMT59D4uYd5oEWx51O7Ps/xd5dDBNdACA9630ymYATHwhaYlQ1SvTb2IbXSnDNrpJhSpVi5yMUQKibdWZ32tdrQCelTCSAAiyCxQpK7ft+9qNpU+zndXSiDfvUJpYhqEPOAvb4iAHNtrOo2BLyAQxhHgdEFlZlkQ+FgjNqbtHkigz01EQ3038ERES6ai9mPAdLvgeghco2/Y6FM2018scNihZsCE/V1q2AVXQ36Q2smaDpWtGCv0ooWUkvKFBUpTc4fOg4Hy0QA4+zpexg5qj+kAJMQK9a0NMdhjLtOfL1Camj1yGGUew4PBDSQOWpWJXsx1d99rjIkRK8Z9H2IwR2xmLt06FniGgBKwLqAljQy4xMIkD9omVOWs6WITQ4Hrg/vUZe6DFkoF+BsNkpfJsSbhLlRDGgQSNIPPugFIdGyg1CTEEtgG8qDBea4Z35KYoQkxSOEipaT516/YTuk4+H0FAjHs9q6vY4l6Vib8qoq6Pom6bmPobcZ9TekfibkDxP3fzJ31UCqguXqXo8YwgIhiDbEGbSFP6QESBmznCRa3US+qOAUX2ynRXn9EdLuIO+Yj4/1KSqSQaB1liB2sQJeA+roPLDsW4WXwLj9Gd0KKEzNUFleY+fIOk5/OozuKsOPvKaZYp/bMQcca2xlPp+BRCpSm5vCftVhfqxNeNJHSQOsAKS0mP64wca6Cc7ZI7mT6rtgzV+Nhmdm8hxQmKt5mZcuBGKyCy8TUHJPnKsc6sArrjJ0Ld4LEMm2C5x7ytElpYha74JIvOLvAvcidzOWiKErUtk9tzUltHINdKFKcmqU0MUN6GLl25O4BMsV7uzsO8zDYTLyNRuofYeEWy1hn7Fc+mP4PEkM+yCoXXbYAAAAASUVORK5CYII=') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAE+klEQVR4nL2XTWgbVxSFP4UXeAMJzIADGpDBU1LomG4k6MIGL6qu4tBFbdJFDF1EECgxXTShi2C8KCKLELxI8wNt3UCLuinWJsSLlqoLg7IIyAUHTRfBY0hhDA7MgwrmQQami5Esjfwb8nM3o7l6uue8c89cvQFgc6OZNBu1JAw2E95x5FqPV5KV76+hdYidd3E/Ok/5s6sYhpF7FwSEDsMUfKxE+G+bxm9VtA6JojAxDOutkxDpRVIxishCEd1RVP+ooZWivf5nMl785K2SONH7YIYgNZjCpFqYpb3RoH5vnubqnbfqDbFfUsaS6sg0nghY/mUBZ61O4LcS2ym9cTVO7J/WcDrAdRVXpmy8p01qSxWaq3eS6L/wjaqxPwGpoeCDaOOYmuoFB601Kw8WqN2/QhS+ORJ7WyA0jAYgVTcRYUq4esnE27GoPaizrBWtRi0pTl0kdzL3Wm0ZIqDBDsD0gai/wpHIMU3xLDiuQ/WbBr7XIlQBycskeR0SWQIyhBEfCAfALSiQ5gSYZsStezbeVkTt3i20Dl/LoH0PCA2jCoTqg492wUXYpypAC9AfGkwuGTQe3mV5qUL7yaMkil7dG30Ctp+VXhpQMLPggAY8GdGSEd5IhPuTRaQClpcq1O9fIdwJXolEv/SIR6bvo2ZqxCGX+AJaElQ3r2SE9TOgbZoX64ThNmGwmVj2e8dqyUALBk1nQUGz64VuKMAbAN+N2EZ3ZjFv1vD+blL7YZ7geftYSmTnQK/vY9AzXS804AtjiBKAhVbTRC8qoGcwbz7Ce7JK7XaF5u8/JsnL6FAiWQLSSvu+B9zCE1ZG+v6XNlHnPMT59D4uYd5oEWx51O7Ps/xd5dDBNdACA9630ymYATHwhaYlQ1SvTb2IbXSnDNrpJhSpVi5yMUQKibdWZ32tdrQCelTCSAAiyCxQpK7ft+9qNpU+zndXSiDfvUJpYhqEPOAvb4iAHNtrOo2BLyAQxhHgdEFlZlkQ+FgjNqbtHkigz01EQ3038ERES6ai9mPAdLvgeghco2/Y6FM2018scNihZsCE/V1q2AVXQ36Q2smaDpWtGCv0ooWUkvKFBUpTc4fOg4Hy0QA4+zpexg5qj+kAJMQK9a0NMdhjLtOfL1Camj1yGGUew4PBDSQOWpWJXsx1d99rjIkRK8Z9H2IwR2xmLt06FniGgBKwLqAljQy4xMIkD9omVOWs6WITQ4Hrg/vUZe6DFkoF+BsNkpfJsSbhLlRDGgQSNIPPugFIdGyg1CTEEtgG8qDBea4Z35KYoQkxSOEipaT516/YTuk4+H0FAjHs9q6vY4l6Vib8qoq6Pom6bmPobcZ9TekfibkDxP3fzJ31UCqguXqXo8YwgIhiDbEGbSFP6QESBmznCRa3US+qOAUX2ynRXn9EdLuIO+Yj4/1KSqSQaB1liB2sQJeA+roPLDsW4WXwLj9Gd0KKEzNUFleY+fIOk5/OozuKsOPvKaZYp/bMQcca2xlPp+BRCpSm5vCftVhfqxNeNJHSQOsAKS0mP64wca6Cc7ZI7mT6rtgzV+Nhmdm8hxQmKt5mZcuBGKyCy8TUHJPnKsc6sArrjJ0Ld4LEMm2C5x7ytElpYha74JIvOLvAvcidzOWiKErUtk9tzUltHINdKFKcmqU0MUN6GLl25O4BMsV7uzsO8zDYTLyNRuofYeEWy1hn7Fc+mP4PEkM+yCoXXbYAAAAASUVORK5CYII=') 2 2, pointer",
    },
    {
        'value': 'imported_banana',
        'label': 'Banana',
        'description': 'Banana kao kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/banana.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAE9ElEQVR4nO2UWYwURRzGf1XVx/TM9Mz2zO6wILAiqzxsBDSgiJooajAqeCRqQpRE4wFRYSOSYDwI0ZDwQiSekRcOD6JGBFHjsYqAbowHqLgciyyH3HvNzB6zMz1dPmyAVQ4VdowPfkmnk6ru+n71/etfQm+IaU4jcUVGnG7+bGUA7Pj25AzVY0vqfRwAYNjMtj9MNC3y+tXomuvGmuMvGD4ls6dx46L3v//p6Lg82cdNi7x+3/3+7Yfvfe3NNUtSyejtfcdPAOhr3p/1nzx28IhMawfrv2u65JQApTIH0LmW5LwpSSZdn6yZP3eqewJAKc0BCvHBPww5v4tJd4RDQ6vix9Y34I+nvVRtZ8QSTe2BIiQ7PS8hxgGfAEhxRUb0fUphDnCoecttbsKivFLK6qq9C95aMceBU3RBf2vZK9MvtfxtU0aPqUAMHMW553mj427mzn8NIL1rw7OjU3lzyNByEDVYsRqSCXXbvwLw0bL7Jjrp7ddeOTKKEYkDHuAStoIRJQf4fPV8Sx36akFVuMDwag9EGAKAIr6vgD5XcSmk2n98xMzsGFU5OIKTCoNyIMiB8Ml0yd1QwgTq3q6tCbd8MdezYWC1i4xHwSgDfPI9Odrago0lA/h81ZNusvOL5ZFim1teGSU8vAJiSZAR0FlaWjppbtYfQAlKsHblHDfesfa1WK7xIitiUVZdgSiLgJ0ADQjB7qaOX3K5oL7fAda9N2N4eXfdMi/XMN5KGMTOTWGkysCOgEyA6uHIkQLbt3fPnz7j5UK/Aax97zHTFQfuqSh89Iyr9qfMAQbOsAHIRDkoAVYYRI5CweeH7/UnmbS54ui/Z3X1bnj3/mREZW9MGjseSahdY1SQQ0ZtrEEpiCbBlGDHQETRaDZusg/Vf+OOe/jRF3edMUD9qmnljmy9LKLaJ3uhfTdErbZBpupBF0CEQ8hkEkJRMA2ww6BcdCDY3EDn1/Xxm6fNXFzXd72/BKhf+aBpic5qS/kXh0OtN5XZBydEnWzKNLugGKDzGh0YyFgMEY1AyARD9cZuuKALNGwz8uvWl906vXbph39e/wSAz5ZOVRGneKFrpy+PONnxUTt9UdjJVluhvGmYPggNBU3QLSAwwQohY2GwZW9TGwosB2QU3y+yeYto/ea7AfdMq122+mQbPAbw6ZK7yj21b+pAd//dZV7HyFCsKGVI9xqiQEu0r0ErdFEihAGOjbAUWAqkBiHBcEBYtLQEfLvJWrdzd2r6Q7PfaDhVwgKg7qUJD1xgNzxRmcoONTxFEYNiIFC2QFoKLU0EEpC9B0tqkAKkBDTCDIEZAg2taWjcae9taEwsbMt6L8x6erl/uhIbr86+av6I3IbHkzEDv0OR3gfNR3wqUgJ3qEIkFRgBGLr3DVDUCF+BECAk+Uw3h9Oaxt/sn5v2e4vbuxKvz5r3TuvpjI8lMGOMytVONG0rppAKcl0Qr5C4lRLlKTAFSIGQEmHK3tCEoFDQpDNw8JAqbtsbWb+ntXJhXiQ+nrNgZf7vGB9LoG1AzcIvf93y+KhzinieIhJXKEMT+AGqR0IAPpDP+3QVBO2dRnAk6+w90BLadKA5XJfuSax/6vnPNsG2f+J7PAGAJ2qvvjoVHL5lkNU8PuV2V0UjWklbkJdmIes7B9I5Z0c6F97a2eNs7SpEf84VQjvnPrem44wc/9d/Tb8DfTW65SgHFxgAAAAASUVORK5CYII=') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAE9ElEQVR4nO2UWYwURRzGf1XVx/TM9Mz2zO6wILAiqzxsBDSgiJooajAqeCRqQpRE4wFRYSOSYDwI0ZDwQiSekRcOD6JGBFHjsYqAbowHqLgciyyH3HvNzB6zMz1dPmyAVQ4VdowPfkmnk6ru+n71/etfQm+IaU4jcUVGnG7+bGUA7Pj25AzVY0vqfRwAYNjMtj9MNC3y+tXomuvGmuMvGD4ls6dx46L3v//p6Lg82cdNi7x+3/3+7Yfvfe3NNUtSyejtfcdPAOhr3p/1nzx28IhMawfrv2u65JQApTIH0LmW5LwpSSZdn6yZP3eqewJAKc0BCvHBPww5v4tJd4RDQ6vix9Y34I+nvVRtZ8QSTe2BIiQ7PS8hxgGfAEhxRUb0fUphDnCoecttbsKivFLK6qq9C95aMceBU3RBf2vZK9MvtfxtU0aPqUAMHMW553mj427mzn8NIL1rw7OjU3lzyNByEDVYsRqSCXXbvwLw0bL7Jjrp7ddeOTKKEYkDHuAStoIRJQf4fPV8Sx36akFVuMDwag9EGAKAIr6vgD5XcSmk2n98xMzsGFU5OIKTCoNyIMiB8Ml0yd1QwgTq3q6tCbd8MdezYWC1i4xHwSgDfPI9Odrago0lA/h81ZNusvOL5ZFim1teGSU8vAJiSZAR0FlaWjppbtYfQAlKsHblHDfesfa1WK7xIitiUVZdgSiLgJ0ADQjB7qaOX3K5oL7fAda9N2N4eXfdMi/XMN5KGMTOTWGkysCOgEyA6uHIkQLbt3fPnz7j5UK/Aax97zHTFQfuqSh89Iyr9qfMAQbOsAHIRDkoAVYYRI5CweeH7/UnmbS54ui/Z3X1bnj3/mREZW9MGjseSahdY1SQQ0ZtrEEpiCbBlGDHQETRaDZusg/Vf+OOe/jRF3edMUD9qmnljmy9LKLaJ3uhfTdErbZBpupBF0CEQ8hkEkJRMA2ww6BcdCDY3EDn1/Xxm6fNXFzXd72/BKhf+aBpic5qS/kXh0OtN5XZBydEnWzKNLugGKDzGh0YyFgMEY1AyARD9cZuuKALNGwz8uvWl906vXbph39e/wSAz5ZOVRGneKFrpy+PONnxUTt9UdjJVluhvGmYPggNBU3QLSAwwQohY2GwZW9TGwosB2QU3y+yeYto/ea7AfdMq122+mQbPAbw6ZK7yj21b+pAd//dZV7HyFCsKGVI9xqiQEu0r0ErdFEihAGOjbAUWAqkBiHBcEBYtLQEfLvJWrdzd2r6Q7PfaDhVwgKg7qUJD1xgNzxRmcoONTxFEYNiIFC2QFoKLU0EEpC9B0tqkAKkBDTCDIEZAg2taWjcae9taEwsbMt6L8x6erl/uhIbr86+av6I3IbHkzEDv0OR3gfNR3wqUgJ3qEIkFRgBGLr3DVDUCF+BECAk+Uw3h9Oaxt/sn5v2e4vbuxKvz5r3TuvpjI8lMGOMytVONG0rppAKcl0Qr5C4lRLlKTAFSIGQEmHK3tCEoFDQpDNw8JAqbtsbWb+ntXJhXiQ+nrNgZf7vGB9LoG1AzcIvf93y+KhzinieIhJXKEMT+AGqR0IAPpDP+3QVBO2dRnAk6+w90BLadKA5XJfuSax/6vnPNsG2f+J7PAGAJ2qvvjoVHL5lkNU8PuV2V0UjWklbkJdmIes7B9I5Z0c6F97a2eNs7SpEf84VQjvnPrem44wc/9d/Tb8DfTW65SgHFxgAAAAASUVORK5CYII=') 2 2, pointer",
    },
    {
        'value': 'imported_macka',
        'label': 'Mačka',
        'description': 'Bijela mačka kao kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/macka.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAB+klEQVR4nLVXwW3rMAx9Dv4GPwMEyAgqoA2YAbpBD84WPviQDXrIEB0gmSACOoIDdIB0BvXQ0p+yTFmSfx9gRJapvEeKpGwA8LUXEa1eswEA7z1qQUSrbDc8qBVxet4tiiAiEBFOz7vo2R95471H0zRFAowxOH3TYPd5nbVpf4iNMcDbR/BsMzWuiYQxJvDOGBP8TsdJAVUiTAvTnnF+j9ed3z1Me04u9xIozOhSzFYBgHHvS70/Pn2vOzYNjpP8kXPHp2a0ldhI8hpoeztn9/GXcL3GiVrdhG63W9E2KI2rnpwhx957307yim1WCyCiiFwTIecT5D5oRBq40/V9DwCw1kY21lo457LnGUkBOcRTslKoAogomziF+/1eLoDJ1xDnYrYVS2gNJAdL3s8KkN5L4loR+/2+TMD/AnvvnEPXdbMdMBIw3Xt5us2ddFqIeX7Je2ChDDViDVJQDjkj6HStwXgtYRiG4CzgjsddMdUB+UrmwJoKyMWvJWG1gJfXW3BfkgO1UI/Zpf0fhiF6J5B5kJMDQRVwrWpteFp2j8djtfdqGTrnsN1uo3lJ2nVd8s+tteOBpjWiSIA05MUSkvRyuYzjw+EQ3EsRKcxGQFPLpPyCwW1WE8pbmYpCg5/3slykvgM5AiwM+BdF7TwoFpArru/7YLu0qH4BZhSYjj5w5ioAAAAASUVORK5CYII=') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAB+klEQVR4nLVXwW3rMAx9Dv4GPwMEyAgqoA2YAbpBD84WPviQDXrIEB0gmSACOoIDdIB0BvXQ0p+yTFmSfx9gRJapvEeKpGwA8LUXEa1eswEA7z1qQUSrbDc8qBVxet4tiiAiEBFOz7vo2R95471H0zRFAowxOH3TYPd5nbVpf4iNMcDbR/BsMzWuiYQxJvDOGBP8TsdJAVUiTAvTnnF+j9ed3z1Me04u9xIozOhSzFYBgHHvS70/Pn2vOzYNjpP8kXPHp2a0ldhI8hpoeztn9/GXcL3GiVrdhG63W9E2KI2rnpwhx957307yim1WCyCiiFwTIecT5D5oRBq40/V9DwCw1kY21lo457LnGUkBOcRTslKoAogomziF+/1eLoDJ1xDnYrYVS2gNJAdL3s8KkN5L4loR+/2+TMD/AnvvnEPXdbMdMBIw3Xt5us2ddFqIeX7Je2ChDDViDVJQDjkj6HStwXgtYRiG4CzgjsddMdUB+UrmwJoKyMWvJWG1gJfXW3BfkgO1UI/Zpf0fhiF6J5B5kJMDQRVwrWpteFp2j8djtfdqGTrnsN1uo3lJ2nVd8s+tteOBpjWiSIA05MUSkvRyuYzjw+EQ3EsRKcxGQFPLpPyCwW1WE8pbmYpCg5/3slykvgM5AiwM+BdF7TwoFpArru/7YLu0qH4BZhSYjj5w5ioAAAAASUVORK5CYII=') 2 2, pointer",
    },
    {
        'value': 'imported_dupin',
        'label': 'Dupin',
        'description': 'Dupin kao kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/dupin.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAADPElEQVR4nMWWMWgbVxjHf6ecQ1Wbg7gZ3h3YuKmqxekgG2QKxVo6eXO7eMjQJQRuMCZjucUiSzwI4UFg6no2hrabO7VotF2QunS5qrSNw/MR40AOuwZLzssg7qyzdIl9ktMPHry77+6+3/2/9773aYDifzQdwCmt0dSHATj8/Vc2NjbeG4AGqGq1ylHaYm93L3QMtU5wd35ha2vr5gGklLiuy1HaCh2/7ewAoJ+f8uTxo5sFAJBS4nkefzdHAPh6Jovrumz8vIN+for/zx+srq4OHCAVTCzLQgjBR6cydGazWZSWonUrjTExyeLi4sABQgUAZmdnASgWixylLc6bZ7w69AD465mMKGEYBr7vDw6gVqshhABgaWkJ27Z5od/l1tBtAF7KZxGIRqPBN9+uRD726tDj4fyXyQACiFwux8HBQRfEcKrF/nPZBTH/8DEAjX2Pp4sPrq1AqvNiamqKer0OgG3bVCoVMh+ecd484+S1zqg1zifjFk19GGNikkwmw0/flWjse2jq9bWDdykQWJAO13XDXF9OR2PfY6h1Eiqxvb2dCCDV66bjOHieRzabRQiBYRihEgCj1jiZMRFWz6TBuwCklEh5sQ1N0wRACIHv+3xxbzTycmZMkM7kEwePAHQGXl9fx3GcCESlUgGIqDBqjQP0VR/0YGJZVpezXq+Ty+UwTRPbtllYWGBzczNSMTNjgn9bk4kBeq6BwDp3RaFQANqKBPUC2ko09eHEKrwV4DJEsVgMQT4eOg6fyc/kMSaSqfBOgABC0zQMwwAuVOiESKrClQA6QcrlMoVCIVycAUR+Jp9oR1wLIIA4Pm4HDQ6j75eXQv/ySvlmAaBdKaenp8P1APDZnbYK/31w91oQ+rsfiYeACxWEEIyMHAP5SGt3FVP9DKWUqtVqam5uTvm+r6SU6oddVy2vlK/0fqIUxJlhGJimyVf5T7lfmHtrKpzSWjjvSwHaXXVPZQI1Lvuc0lrn/f4BlFI9IQKfU1rrCi6lVIDq2Q8kMaUUmqbF+n7c+xOAz8faZ0jn2dO3Ap1/G+cL/vjyGOgijFMAwHXdWN/AFIgb1Wo1VoHEheiqFjQ6vfoNiGlK36e9ASsECgq3E/t0AAAAAElFTkSuQmCC') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAADPElEQVR4nMWWMWgbVxjHf6ecQ1Wbg7gZ3h3YuKmqxekgG2QKxVo6eXO7eMjQJQRuMCZjucUiSzwI4UFg6no2hrabO7VotF2QunS5qrSNw/MR40AOuwZLzssg7qyzdIl9ktMPHry77+6+3/2/9773aYDifzQdwCmt0dSHATj8/Vc2NjbeG4AGqGq1ylHaYm93L3QMtU5wd35ha2vr5gGklLiuy1HaCh2/7ewAoJ+f8uTxo5sFAJBS4nkefzdHAPh6Jovrumz8vIN+for/zx+srq4OHCAVTCzLQgjBR6cydGazWZSWonUrjTExyeLi4sABQgUAZmdnASgWixylLc6bZ7w69AD465mMKGEYBr7vDw6gVqshhABgaWkJ27Z5od/l1tBtAF7KZxGIRqPBN9+uRD726tDj4fyXyQACiFwux8HBQRfEcKrF/nPZBTH/8DEAjX2Pp4sPrq1AqvNiamqKer0OgG3bVCoVMh+ecd484+S1zqg1zifjFk19GGNikkwmw0/flWjse2jq9bWDdykQWJAO13XDXF9OR2PfY6h1Eiqxvb2dCCDV66bjOHieRzabRQiBYRihEgCj1jiZMRFWz6TBuwCklEh5sQ1N0wRACIHv+3xxbzTycmZMkM7kEwePAHQGXl9fx3GcCESlUgGIqDBqjQP0VR/0YGJZVpezXq+Ty+UwTRPbtllYWGBzczNSMTNjgn9bk4kBeq6BwDp3RaFQANqKBPUC2ko09eHEKrwV4DJEsVgMQT4eOg6fyc/kMSaSqfBOgABC0zQMwwAuVOiESKrClQA6QcrlMoVCIVycAUR+Jp9oR1wLIIA4Pm4HDQ6j75eXQv/ySvlmAaBdKaenp8P1APDZnbYK/31w91oQ+rsfiYeACxWEEIyMHAP5SGt3FVP9DKWUqtVqam5uTvm+r6SU6oddVy2vlK/0fqIUxJlhGJimyVf5T7lfmHtrKpzSWjjvSwHaXXVPZQI1Lvuc0lrn/f4BlFI9IQKfU1rrCi6lVIDq2Q8kMaUUmqbF+n7c+xOAz8faZ0jn2dO3Ap1/G+cL/vjyGOgijFMAwHXdWN/AFIgb1Wo1VoHEheiqFjQ6vfoNiGlK36e9ASsECgq3E/t0AAAAAElFTkSuQmCC') 2 2, pointer",
    },
    {
        'value': 'imported_bijeli_noz',
        'label': 'Bijeli nož',
        'description': 'Bijeli nož kao kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/bijeli_noz.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABW0lEQVR4nMWW4a2EIBCEh8t1hK3YAleLJUgJtmALS03cj/fwlhUUOfAmMTFowufsLKsC4PFDPcMNEQEApmkCACzLAqXULRA+pXEct3v8udTrgl/X9ZcQ8UIOpiMEPBF5Ito2uRPikQgErLWprGzPW8tDuHAqmvs54Jw7R9YGnuavvxwANoBhGCKIEpAWEJEDHCKA9IbYlaAYQpsmEAoHsyAczwCgtd6/4OJuUcPrMsDOAS6Zi52YC0CdE4cOBHEnAOFGcEHAlA6yIoAshEscWAykBKIYIAkBVhbhQCnEJYAsRGbzEpDLAAAwm7gjjDHVEIddkNPLJjrC2XQmmFKDrApAQkTT8yJENcAhxIk4RFUGpGozAWe/c6CFmgDIUDro80n6n5XmDmjzmQfhv4LDSLAmGeCSB5WUs/HEbA6Qg5AbB90SwtzmtwHwXEh1KUGQLEXKiedupYOOSvAGkyeucgh4ux0AAAAASUVORK5CYII=') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABW0lEQVR4nMWW4a2EIBCEh8t1hK3YAleLJUgJtmALS03cj/fwlhUUOfAmMTFowufsLKsC4PFDPcMNEQEApmkCACzLAqXULRA+pXEct3v8udTrgl/X9ZcQ8UIOpiMEPBF5Ito2uRPikQgErLWprGzPW8tDuHAqmvs54Jw7R9YGnuavvxwANoBhGCKIEpAWEJEDHCKA9IbYlaAYQpsmEAoHsyAczwCgtd6/4OJuUcPrMsDOAS6Zi52YC0CdE4cOBHEnAOFGcEHAlA6yIoAshEscWAykBKIYIAkBVhbhQCnEJYAsRGbzEpDLAAAwm7gjjDHVEIddkNPLJjrC2XQmmFKDrApAQkTT8yJENcAhxIk4RFUGpGozAWe/c6CFmgDIUDro80n6n5XmDmjzmQfhv4LDSLAmGeCSB5WUs/HEbA6Qg5AbB90SwtzmtwHwXEh1KUGQLEXKiedupYOOSvAGkyeucgh4ux0AAAAASUVORK5CYII=') 2 2, pointer",
    },
    {
        'value': 'imported_ljubicasti_morski_pas',
        'label': 'Ljubičasti morski pas',
        'description': 'Ljubičasti morski pas kao kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/ljubicasti_morski_pas.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,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') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,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') 2 2, pointer",
    },
    {
        'value': 'imported_ruza',
        'label': 'Ruža',
        'description': 'Ruža kao kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/ruza.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAEc0lEQVR4nMXXbWxTVRzH8W9vn7tubQdDMp46AokEYxsSo+/oXojGNzRREqOJq9H4At+UYDCGCA0JPkVjiQmKCdmAKCISt6gJiIldgkTAQGfYVBjbWugcfbi7t2t7e2+ffKHEZrDIw2X+3t17c87/k3PPPeceuIOUPz81Lr520HUnbf4rptk3Um98ssLh9PhtLlcsfuSbsGPNqoDv0y3dyt7vd1qXLPCqo1N+YFAvgKH5YnjT6y5X13KpUlRRivVY7koqsKTbF1+2amWfwWyMGhe0YtjwsGGuzu4mAkD9qzMupfeHD9u8yyTbwg7a1z5Io94IFP8UUSZz/sK0GFYkiVpBof7dhZ26A4RnHpXliaT3+sVrTF/NkhkZZyo+is3TiiYWyFwc9Y4fP8nYtyeoqGpIdwDA9KXRvvxkgtTPI4zH4pSlAma7FYvTjmNxB551flLDI0z9dNYr7jm2QnfAmsNvDYxJyfD5sTjFKREaQKNBowGC2Yxz+RLWvtJD4vwFlJzo1QtgOvfk9t7EqV9DnpWdOBa2YbJZcHS4uXp6GK2kospFZiazWDxOLO1teFavJnlSt48A4ZHju1+sliteRZyZqJYr2NvbaF+5lPy1LIqYp5ieRp6YIn3+Mg1FpX11FwaDIa4bAODZ6vGE2WENGQQDRosZs91KV7efUloin8oiJdJM/vIH4kgCwWiJP3b6kKwrAOCJS72DNa0aU3J5ZiazdAXWkaFIMS0hJ68jJ64zduIcP57pl/QqDrMWoti6zS7BYpqwtjnclhY7yatJzDmNslQAYLjzMme6LmK04x04SkJ3AMDJNS/5gH7AW1UrlOUip4y/I28cY8ak9DUgZG4h+Nn7DOgBuGkvePy3/UNA18CiTb6aVnUPbzgbbH0qFa7L8JDH2zecnMBoxA/3CXAjG9NHhwB2b0QSIOy0WSX3IlfUM0O4ViegR3FomoRzZfvzDOVy9KczakjMZNyd7s6AIMwjACCXJaTkCaauTIYwVSMLPQbePowuy/FtAQ7sQu5YRqTVi1uckqJGs9VbSOtR/i7z5kdc2H2Ir/Xo67ZGYHZKOQL1Cv7IPnr/F8AHEWQpSVAwEnzvKD3zDvgHMSRfI1CWid4L4p7/77ZG8LmWEhNMRC+PEa3XCNU1gnUN6hr9Rz5mz30F3EA4FhNLi9Bo4K7VoKpBpQyNCv7Dexiaq+2cK2Fztu3FZbMRtdqIbX+OA7Ofa06olqDFidsA1GqgaVA2Q6VMCNgyV993NAI7e+mpVAhlU/TXjMT272Bo87v4LBZiNjtuiwUEAapVUFUoFUBMIik5/P1f3Hr3vKtX8PQLrDe7CJmdhByt0NoGLS1gtUG9DmUFJAnkDGh5qBaJHTtIt26AG+nZgctqJWS3E7TaCJhM0GhApfI3olQCtQCVPHy579a1dD3lNCccZYVaJlQuEfC04HcvILzj5Zvnz30DNGdrBF9LB1GTFaoqkV2v/nu2nBdAE2S9zUWf0cKEViTyzjYG5xXQDHE+QLiq4v0LRNTe9ADFZecAAAAASUVORK5CYII=') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAEc0lEQVR4nMXXbWxTVRzH8W9vn7tubQdDMp46AokEYxsSo+/oXojGNzRREqOJq9H4At+UYDCGCA0JPkVjiQmKCdmAKCISt6gJiIldgkTAQGfYVBjbWugcfbi7t2t7e2+ffKHEZrDIw2X+3t17c87/k3PPPeceuIOUPz81Lr520HUnbf4rptk3Um98ssLh9PhtLlcsfuSbsGPNqoDv0y3dyt7vd1qXLPCqo1N+YFAvgKH5YnjT6y5X13KpUlRRivVY7koqsKTbF1+2amWfwWyMGhe0YtjwsGGuzu4mAkD9qzMupfeHD9u8yyTbwg7a1z5Io94IFP8UUSZz/sK0GFYkiVpBof7dhZ26A4RnHpXliaT3+sVrTF/NkhkZZyo+is3TiiYWyFwc9Y4fP8nYtyeoqGpIdwDA9KXRvvxkgtTPI4zH4pSlAma7FYvTjmNxB551flLDI0z9dNYr7jm2QnfAmsNvDYxJyfD5sTjFKREaQKNBowGC2Yxz+RLWvtJD4vwFlJzo1QtgOvfk9t7EqV9DnpWdOBa2YbJZcHS4uXp6GK2kospFZiazWDxOLO1teFavJnlSt48A4ZHju1+sliteRZyZqJYr2NvbaF+5lPy1LIqYp5ieRp6YIn3+Mg1FpX11FwaDIa4bAODZ6vGE2WENGQQDRosZs91KV7efUloin8oiJdJM/vIH4kgCwWiJP3b6kKwrAOCJS72DNa0aU3J5ZiazdAXWkaFIMS0hJ68jJ64zduIcP57pl/QqDrMWoti6zS7BYpqwtjnclhY7yatJzDmNslQAYLjzMme6LmK04x04SkJ3AMDJNS/5gH7AW1UrlOUip4y/I28cY8ak9DUgZG4h+Nn7DOgBuGkvePy3/UNA18CiTb6aVnUPbzgbbH0qFa7L8JDH2zecnMBoxA/3CXAjG9NHhwB2b0QSIOy0WSX3IlfUM0O4ViegR3FomoRzZfvzDOVy9KczakjMZNyd7s6AIMwjACCXJaTkCaauTIYwVSMLPQbePowuy/FtAQ7sQu5YRqTVi1uckqJGs9VbSOtR/i7z5kdc2H2Ir/Xo67ZGYHZKOQL1Cv7IPnr/F8AHEWQpSVAwEnzvKD3zDvgHMSRfI1CWid4L4p7/77ZG8LmWEhNMRC+PEa3XCNU1gnUN6hr9Rz5mz30F3EA4FhNLi9Bo4K7VoKpBpQyNCv7Dexiaq+2cK2Fztu3FZbMRtdqIbX+OA7Ofa06olqDFidsA1GqgaVA2Q6VMCNgyV993NAI7e+mpVAhlU/TXjMT272Bo87v4LBZiNjtuiwUEAapVUFUoFUBMIik5/P1f3Hr3vKtX8PQLrDe7CJmdhByt0NoGLS1gtUG9DmUFJAnkDGh5qBaJHTtIt26AG+nZgctqJWS3E7TaCJhM0GhApfI3olQCtQCVPHy579a1dD3lNCccZYVaJlQuEfC04HcvILzj5Zvnz30DNGdrBF9LB1GTFaoqkV2v/nu2nBdAE2S9zUWf0cKEViTyzjYG5xXQDHE+QLiq4v0LRNTe9ADFZecAAAAASUVORK5CYII=') 2 2, pointer",
    },
    {
        'value': 'imported_list',
        'label': 'List',
        'description': 'Zeleni list kao kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/list.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAo0lEQVR4nO2WsQ2AIBBFv8aF3MNdHMElHMUJHMDKlsTKjsLaQisaE+VzgiTmfg/v3YX8UAA4kDFlTrgKqMD/BAbTop/qoDNVDKjLso2w6/6NgAMv2yi9QiYQCywSGEz7CLbrjq6ZgwToR+iDS0MJpILTAkwk66cEUk5PCTCRTg+8LCJXOlK4V+Bu/THAlEBKMCVw7faYYJcC+ilVARVQARXInBPpIk7UXAHeCQAAAABJRU5ErkJggg==') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAo0lEQVR4nO2WsQ2AIBBFv8aF3MNdHMElHMUJHMDKlsTKjsLaQisaE+VzgiTmfg/v3YX8UAA4kDFlTrgKqMD/BAbTop/qoDNVDKjLso2w6/6NgAMv2yi9QiYQCywSGEz7CLbrjq6ZgwToR+iDS0MJpILTAkwk66cEUk5PCTCRTg+8LCJXOlK4V+Bu/THAlEBKMCVw7faYYJcC+ilVARVQARXInBPpIk7UXAHeCQAAAABJRU5ErkJggg==') 2 2, pointer",
    },
    {
        'value': 'imported_ruka',
        'label': 'Ruka',
        'description': 'Ruka koja pokazuje prstom.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/ruka.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABWklEQVR4nMWVURKDIAxEV6c3kjPJmeiZyJnoR42NEDBa1J3pdKxT9mUJAQBSiiEBeOQzYlGKAU9olA9PQIwAMDj/GMSo/XgnxAogU7gTYsC3G5vGOVxPFVugmV2ZhtoDOQQRIYb5EoBiC6TY1Pk3gF8Svbdkd1qlGFIM8+a51/R8NcliABGtFcte6JWCCmAx7gVT9EAMc7HnNePNQich1CY8YgwAmCZAJHZE1R4wGQtzTNOpU6LOAVZtKm4MFvP12wJtBWgaS/0BYQbQgHpAmAAG5xHD3B7H0vwARPUU1JqQiNZjWrzPIZRCclUvI66W957/PC2V8XuSRkoCeWEmAOB7AbFJDiO3Qqaxl4AG0bwNpXhC8gJcOYNyMi3zjfGSqBkglwQpIIwanD8PkINoi++eAOfro9iq1tglot1UTg8ii5x/b0/J3QAtCE7ucoAWBPDHKeilWxJo6QMK1B4AhsuFdwAAAABJRU5ErkJggg==') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABWklEQVR4nMWVURKDIAxEV6c3kjPJmeiZyJnoR42NEDBa1J3pdKxT9mUJAQBSiiEBeOQzYlGKAU9olA9PQIwAMDj/GMSo/XgnxAogU7gTYsC3G5vGOVxPFVugmV2ZhtoDOQQRIYb5EoBiC6TY1Pk3gF8Svbdkd1qlGFIM8+a51/R8NcliABGtFcte6JWCCmAx7gVT9EAMc7HnNePNQich1CY8YgwAmCZAJHZE1R4wGQtzTNOpU6LOAVZtKm4MFvP12wJtBWgaS/0BYQbQgHpAmAAG5xHD3B7H0vwARPUU1JqQiNZjWrzPIZRCclUvI66W957/PC2V8XuSRkoCeWEmAOB7AbFJDiO3Qqaxl4AG0bwNpXhC8gJcOYNyMi3zjfGSqBkglwQpIIwanD8PkINoi++eAOfro9iq1tglot1UTg8ii5x/b0/J3QAtCE7ucoAWBPDHKeilWxJo6QMK1B4AhsuFdwAAAABJRU5ErkJggg==') 2 2, pointer",
    },
    {
        'value': 'imported_gitara',
        'label': 'Gitara',
        'description': 'Crvena gitara kao kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/gitara.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACcElEQVR4nLWW65GrMAyFP9/ZBraFtGCXQAtQgimBlEBKgBKcEpYSRAtpYUvQ/QFOzCsLk0QzmiGyYx0dPWyjKspMjHEAqMr9+2MyApioqmi0r62/U79SMFVVAUsGPs3EJGJA67pWa/2EgQ8yMaUe0Kqq7kA+7Fz/PaPmfD6Dtcc5PSCbAGI90PcUxQVV+RiIRQrW1Fr/kVSY8eOBZhbptPq/Uf15a0d8zQ3zw2MLhhC43W4YU769Lf+kKVIfuyK1vUH3bfwUiEUKtiSdiI90rE/JWEd703QIcYw6hLA6qFRFBbTaz9Bx2rbSoSqqHhVQ9cP6DhDHnad3x5wJ9ahIo+rRfAcLT0fxIlcq9MZxvd7uv4uiACDPc4xx9O2wt28heLhcOlTl6STdHXmkVsbIUyYiC3meq0gz6Lg/55GOFUb2A8gTAHPNsmwAYb167xcgIpAIPJ67uw0BbF3Tn89Yz4PqxmOtpQacK6nr+p4iAKShB3AlwTOkLIRJ+x4qwLqul0zEaKXR0+l0//beqkijJHvmTCwuo78kFlNhHFW6IM1kX9u2eO8nNudKRBpwJRcgqGy/B7bEGDdMQxUugI0+XPnUOTA4n8lhAKn4nx/aPgER7Ynzvu/BlXSuHEAmQF8CYIwjy76xfWKcHY4r+S1bOiCThm7lnENdsCa3EKAoHp2RgOiA77FLOleSJf+zdf06gHgb9hvrGdBFBhL7BaiywfJSDUTpxmjmtRBBzJ3nIWDtWNAcbMM1URUK4wgrAOLASp3n+WnyVnj5VUMyqtfGdD6qyPIueAsDKRPX643reENGiVHD8pX0VgARxJpsPc/+A3bANA1oeYvCAAAAAElFTkSuQmCC') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACcElEQVR4nLWW65GrMAyFP9/ZBraFtGCXQAtQgimBlEBKgBKcEpYSRAtpYUvQ/QFOzCsLk0QzmiGyYx0dPWyjKspMjHEAqMr9+2MyApioqmi0r62/U79SMFVVAUsGPs3EJGJA67pWa/2EgQ8yMaUe0Kqq7kA+7Fz/PaPmfD6Dtcc5PSCbAGI90PcUxQVV+RiIRQrW1Fr/kVSY8eOBZhbptPq/Uf15a0d8zQ3zw2MLhhC43W4YU769Lf+kKVIfuyK1vUH3bfwUiEUKtiSdiI90rE/JWEd703QIcYw6hLA6qFRFBbTaz9Bx2rbSoSqqHhVQ9cP6DhDHnad3x5wJ9ahIo+rRfAcLT0fxIlcq9MZxvd7uv4uiACDPc4xx9O2wt28heLhcOlTl6STdHXmkVsbIUyYiC3meq0gz6Lg/55GOFUb2A8gTAHPNsmwAYb167xcgIpAIPJ67uw0BbF3Tn89Yz4PqxmOtpQacK6nr+p4iAKShB3AlwTOkLIRJ+x4qwLqul0zEaKXR0+l0//beqkijJHvmTCwuo78kFlNhHFW6IM1kX9u2eO8nNudKRBpwJRcgqGy/B7bEGDdMQxUugI0+XPnUOTA4n8lhAKn4nx/aPgER7Ynzvu/BlXSuHEAmQF8CYIwjy76xfWKcHY4r+S1bOiCThm7lnENdsCa3EKAoHp2RgOiA77FLOleSJf+zdf06gHgb9hvrGdBFBhL7BaiywfJSDUTpxmjmtRBBzJ3nIWDtWNAcbMM1URUK4wgrAOLASp3n+WnyVnj5VUMyqtfGdD6qyPIueAsDKRPX643reENGiVHD8pX0VgARxJpsPc/+A3bANA1oeYvCAAAAAElFTkSuQmCC') 2 2, pointer",
    },
    {
        'value': 'imported_crna_strelica',
        'label': 'Crna strelica',
        'description': 'Crna strelica kao kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/crna_strelica.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACPElEQVR4nO3WO2hUQRQG4C/GmMRnCKgETBEf4AMsBEHxWYiVlQoWgoraiWhnYZXCxlJQsQqIFlaiCKKCIIKPTgU1SixEER9JfCTRTbLZtTiz7LLYuHuTKj9cZpi5d85///+cmaGMRrRhlilEQ2oX4AS24gvu4ja+ThWRnfiEAooYwh3sQ+tUENiLkRS8gDHkhQI92IAZk0lgMz6m4BMYr3jyeIOzWKtsW6bowOMqAnn8wWjq5/ACZ7AyawLNuK5sQYnIAN7iZyIyJvLjIQ6ivd7AJV/zGE5tIY0V0YRXuIrXiQSswklROR1ZECiI8iuKPx8S8jdiPX7hGM6hF7+FauvUmaClD4voE943JDLPhCLtOIClOI0juJze/yBsyaRCduCbUOMdjuO+UGJM/Pmm9O5sUTnbsCiL4LBa+F3Ad+xJAXqF9zncVKfn1aiUblB5621FJx7gfAoOW0T2Z7YXVBIYQn/qN2Je6vfghsiTVhzG9skgMCqyvZjG56fxYaFCX5rrFBXRljWBPD6ntgFdmJvmnuKSOC8asBtXsiBQjf0iF3Ip6PKKuXahUmmnzGFXvQGr6/e5OHgG8ENIXsKguCeUMAvd/1ijLrSIjeYCjop6r8QSUSklFboxJ0sChO9dyklYjVO4JU7Pa9hYT7Ba6rkJh4T/jXiCi8K2/0Yt/o3jnjimJ8TdoOYDqdYEei/uBCMiGddgYS0LzayRQBGPsAyLxQbWUstC9e7pK9LTj5dCkSlHs9qVnMY0puEvBiaYuZdKC6gAAAAASUVORK5CYII=') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAACPElEQVR4nO3WO2hUQRQG4C/GmMRnCKgETBEf4AMsBEHxWYiVlQoWgoraiWhnYZXCxlJQsQqIFlaiCKKCIIKPTgU1SixEER9JfCTRTbLZtTiz7LLYuHuTKj9cZpi5d85///+cmaGMRrRhlilEQ2oX4AS24gvu4ja+ThWRnfiEAooYwh3sQ+tUENiLkRS8gDHkhQI92IAZk0lgMz6m4BMYr3jyeIOzWKtsW6bowOMqAnn8wWjq5/ACZ7AyawLNuK5sQYnIAN7iZyIyJvLjIQ6ivd7AJV/zGE5tIY0V0YRXuIrXiQSswklROR1ZECiI8iuKPx8S8jdiPX7hGM6hF7+FauvUmaClD4voE943JDLPhCLtOIClOI0juJze/yBsyaRCduCbUOMdjuO+UGJM/Pmm9O5sUTnbsCiL4LBa+F3Ad+xJAXqF9zncVKfn1aiUblB5621FJx7gfAoOW0T2Z7YXVBIYQn/qN2Je6vfghsiTVhzG9skgMCqyvZjG56fxYaFCX5rrFBXRljWBPD6ntgFdmJvmnuKSOC8asBtXsiBQjf0iF3Ip6PKKuXahUmmnzGFXvQGr6/e5OHgG8ENIXsKguCeUMAvd/1ijLrSIjeYCjop6r8QSUSklFboxJ0sChO9dyklYjVO4JU7Pa9hYT7Ba6rkJh4T/jXiCi8K2/0Yt/o3jnjimJ8TdoOYDqdYEei/uBCMiGddgYS0LzayRQBGPsAyLxQbWUstC9e7pK9LTj5dCkSlHs9qVnMY0puEvBiaYuZdKC6gAAAAASUVORK5CYII=') 2 2, pointer",
    },
    {
        'value': 'imported_crveni_noz',
        'label': 'Crveni nož',
        'description': 'Crveni nož kao kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/crveni_noz.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAC4UlEQVR4nO3UTUgUYRzH8Z/avo3PqqMz2+qquS6ioWBJLm5uYoZGQm5oh96EyGuHSDoUdehidehQUIcuUURGYGQSlYfEMgmj1wXNlyzD3NzR1aXV2ZnZZ6ZLgVASKbte9nv8P/A8H54HHgBAEpCHtayhuPi+a8OGnWtxdiIAGIzGl0fd7oee3Nzja4FAUVLSxmuFhVp7QYF2oLT0uh3Qx+rsRAD4SOnQV0EYZoJBVJvNh+tdrqebCVkfMwAAjEYit5GdjcjkJCyjo5U7eP6V22zeFDPA21DoxndRpDkWCziOQ/7iYk5DaupzT2bmnpgARlR14ltGxhN9WhqSWBY/GAb8/v2kvq6uo6W5+WTUAQDQPTV1lW7bBtZuR6S2Fr6REUgsm1hdVdV2orW1XQcYowpIHB9/9HpiYoyvqQHDcVhISMAigPlgEJvKyvadv3ix12Gz2aIG6AfU3v7+c4G+PuQTAiUchqxpkADMzMyA4zjn2QsXBqrLyyuiAgAAcXDw1sC9e18TxsZgN5sBkwmKokCWZczOzkJRlKzTbW09exsaDkYF8AKQ36xbdyocCCBLkpDOstA0DZRSyLIMQRAgK4rR6XbfzLbZui0WS+lqAAnLLRzl+b7tFRWVupISvJMkIC0NAKCqKiKRCO60tyMsSXA4HMGhoaGtfr9/cCWAP27gdw8DgZZPhCxoqoqSoiKIc3MIiyL8fn/4QWfnY78gqKFQCD6fL9XpdN7leX5F3/eygM+UDnf19BwTRBFsbi7y0tMx7PW+f9TVteWD17tL0zQPpVSZnp6GJEnFVqv12EoA/6w+I+PS5d271SaX6woDGJauJScnnyGEaFarVfN4PALLskxUEHlGY9Xf5iaTiTAMEySEaI2NjVpKSsqR/9172SdY2pdw+Nnf5qIohiilHZRS+Hw+GAyGpv8FrDqdTufQ6/XzhBCN47ixmAN+IfL1ev0hg8FgXxNAvHjx4sVbTT8BdA0WMLt/31oAAAAASUVORK5CYII=') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAC4UlEQVR4nO3UTUgUYRzH8Z/avo3PqqMz2+qquS6ioWBJLm5uYoZGQm5oh96EyGuHSDoUdehidehQUIcuUURGYGQSlYfEMgmj1wXNlyzD3NzR1aXV2ZnZZ6ZLgVASKbte9nv8P/A8H54HHgBAEpCHtayhuPi+a8OGnWtxdiIAGIzGl0fd7oee3Nzja4FAUVLSxmuFhVp7QYF2oLT0uh3Qx+rsRAD4SOnQV0EYZoJBVJvNh+tdrqebCVkfMwAAjEYit5GdjcjkJCyjo5U7eP6V22zeFDPA21DoxndRpDkWCziOQ/7iYk5DaupzT2bmnpgARlR14ltGxhN9WhqSWBY/GAb8/v2kvq6uo6W5+WTUAQDQPTV1lW7bBtZuR6S2Fr6REUgsm1hdVdV2orW1XQcYowpIHB9/9HpiYoyvqQHDcVhISMAigPlgEJvKyvadv3ix12Gz2aIG6AfU3v7+c4G+PuQTAiUchqxpkADMzMyA4zjn2QsXBqrLyyuiAgAAcXDw1sC9e18TxsZgN5sBkwmKokCWZczOzkJRlKzTbW09exsaDkYF8AKQ36xbdyocCCBLkpDOstA0DZRSyLIMQRAgK4rR6XbfzLbZui0WS+lqAAnLLRzl+b7tFRWVupISvJMkIC0NAKCqKiKRCO60tyMsSXA4HMGhoaGtfr9/cCWAP27gdw8DgZZPhCxoqoqSoiKIc3MIiyL8fn/4QWfnY78gqKFQCD6fL9XpdN7leX5F3/eygM+UDnf19BwTRBFsbi7y0tMx7PW+f9TVteWD17tL0zQPpVSZnp6GJEnFVqv12EoA/6w+I+PS5d271SaX6woDGJauJScnnyGEaFarVfN4PALLskxUEHlGY9Xf5iaTiTAMEySEaI2NjVpKSsqR/9172SdY2pdw+Nnf5qIohiilHZRS+Hw+GAyGpv8FrDqdTufQ6/XzhBCN47ixmAN+IfL1ev0hg8FgXxNAvHjx4sVbTT8BdA0WMLt/31oAAAAASUVORK5CYII=') 2 2, pointer",
    },
    {
        'value': 'imported_srce',
        'label': 'Srce',
        'description': 'Rozo srce kao kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/srce.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAELUlEQVR4nO2Wy2/cVBSHv3PtNGnStEnDBAqCIhBUQIEFQmxYsgM14iEkVogl6d/TCJb8A0jpEiSQUKtKiEVVlafoIyltM690Mm+P7fvrwm4yncx00kTseiRb9r3n3vP5+Dyulb767gOi5GWwQySpo5cEgAelQKwwaCF18WogGhhb8qobqiFiIAXSp8+fTdmHhOb9mzwz/3Eq9xSOgDRFSSqSVERxlziNSNKmpWmNVFXzqjloIKsCGxgVRLl0ZmUTaIM6i48BE5rZzNSnb53yzhZ9MyJtRqjVxbcjqd0zdWLUjvHNCFo9Tyfesii562J/De+vm7gJFM1oS2wCxfLSSgWoF1aXk3EADq/QJoLwkVoGNhFgU6Gz6Yl5zRx6zU+FH/kw+FLOPgfekThqxgLwKvA68GJ5aeXIeID9isMIbE7O3vPGF8D7wOF89gjwPPBSeWll7v8B2BZzmJ2Q8YngNBDkEwEwD5wsL63MjgPQQSmABeBDYGZgfBZ4try0MjkcwIjV7fUASSiH0fZdEqD8QULKifPxfF02eRqYV67dd81LmiudOWe7AOz4dJtuEgNmhuXUtn03M8DyBzPM8k/Lx/N1ZmZGAMxZrp1fD2Send+zA6BEHd/qdfbh9mHigVF7Hc4/7mEA0rSuRqfFweMA4A5QHTEXjgBQTdVWHbMDAigCfgQaoxSGDTqcVXyxUTdn8QGsd4AfgAtAb4RONAwiJE7LqnfbNLp1oDDWlACvPwkcJJqW+aJDFw2uGGw9wo0NshgZAAiDe2pF5fR2bUMnji3w4D/tpGH+mm9twppR0yX+WzM8XjGQAGmemnnmPoQcAZVhTcqp00sUJWu6Uys5R8xe0jBw0y5j0WDKAQyMJWa2YWbtYW5xdOMEr3VfrFfViDax8dlgUn+kK3ft4DoPtIBbQKmwurzL/ZDFQEwYrGmjUdWNyjU7uXBMO01lt3jfscRfGTBUzI1NkXmwC9SBCrBVWF0eeT4IC99/nZY/+6aoKCmlv9/9O5iZPMb0xClgYpe2iKyTXDCv632jjizA/iGrdA6IgWgv54HsHJD4OsaaKq3Z9Le1X93bzyWaDF9R1lYz0/L3rBVddO3eJVCnr6YYmcdUWF2ujzM4HEA0gXXQGyo1qukv//7M4uxld3SqoNRPqN6tWq1zi3ZcMakjMVjTQobU+T0DFFaX49KZc+tAGXGcTtxlbfMWcANILE8zIBmRaj0ytz+2bB9IzOy2mf1hZnGeTf3d7KHU6pvDzFIza5hZdCCAwupyG7gMrLP3xiRgiyzN9tVLBo9k/wGXyDraXjbsAteBzf0Y3wWQf8VfwE/AvTFr28BV4Oaj8nyc7OrPAOWllVDSCTN7F3iBrCakZMHYlLRuZleBamF1+SBddDhAH8gUMElWDybJXN6UFC2eP7uvoHsiT2RQ7gOhQzXK+5OubAAAAABJRU5ErkJggg==') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAELUlEQVR4nO2Wy2/cVBSHv3PtNGnStEnDBAqCIhBUQIEFQmxYsgM14iEkVogl6d/TCJb8A0jpEiSQUKtKiEVVlafoIyltM690Mm+P7fvrwm4yncx00kTseiRb9r3n3vP5+Dyulb767gOi5GWwQySpo5cEgAelQKwwaCF18WogGhhb8qobqiFiIAXSp8+fTdmHhOb9mzwz/3Eq9xSOgDRFSSqSVERxlziNSNKmpWmNVFXzqjloIKsCGxgVRLl0ZmUTaIM6i48BE5rZzNSnb53yzhZ9MyJtRqjVxbcjqd0zdWLUjvHNCFo9Tyfesii562J/De+vm7gJFM1oS2wCxfLSSgWoF1aXk3EADq/QJoLwkVoGNhFgU6Gz6Yl5zRx6zU+FH/kw+FLOPgfekThqxgLwKvA68GJ5aeXIeID9isMIbE7O3vPGF8D7wOF89gjwPPBSeWll7v8B2BZzmJ2Q8YngNBDkEwEwD5wsL63MjgPQQSmABeBDYGZgfBZ4try0MjkcwIjV7fUASSiH0fZdEqD8QULKifPxfF02eRqYV67dd81LmiudOWe7AOz4dJtuEgNmhuXUtn03M8DyBzPM8k/Lx/N1ZmZGAMxZrp1fD2Send+zA6BEHd/qdfbh9mHigVF7Hc4/7mEA0rSuRqfFweMA4A5QHTEXjgBQTdVWHbMDAigCfgQaoxSGDTqcVXyxUTdn8QGsd4AfgAtAb4RONAwiJE7LqnfbNLp1oDDWlACvPwkcJJqW+aJDFw2uGGw9wo0NshgZAAiDe2pF5fR2bUMnji3w4D/tpGH+mm9twppR0yX+WzM8XjGQAGmemnnmPoQcAZVhTcqp00sUJWu6Uys5R8xe0jBw0y5j0WDKAQyMJWa2YWbtYW5xdOMEr3VfrFfViDax8dlgUn+kK3ft4DoPtIBbQKmwurzL/ZDFQEwYrGmjUdWNyjU7uXBMO01lt3jfscRfGTBUzI1NkXmwC9SBCrBVWF0eeT4IC99/nZY/+6aoKCmlv9/9O5iZPMb0xClgYpe2iKyTXDCv632jjizA/iGrdA6IgWgv54HsHJD4OsaaKq3Z9Le1X93bzyWaDF9R1lYz0/L3rBVddO3eJVCnr6YYmcdUWF2ujzM4HEA0gXXQGyo1qukv//7M4uxld3SqoNRPqN6tWq1zi3ZcMakjMVjTQobU+T0DFFaX49KZc+tAGXGcTtxlbfMWcANILE8zIBmRaj0ytz+2bB9IzOy2mf1hZnGeTf3d7KHU6pvDzFIza5hZdCCAwupyG7gMrLP3xiRgiyzN9tVLBo9k/wGXyDraXjbsAteBzf0Y3wWQf8VfwE/AvTFr28BV4Oaj8nyc7OrPAOWllVDSCTN7F3iBrCakZMHYlLRuZleBamF1+SBddDhAH8gUMElWDybJXN6UFC2eP7uvoHsiT2RQ7gOhQzXK+5OubAAAAABJRU5ErkJggg==') 2 2, pointer",
    },
    {
        'value': 'imported_plamen',
        'label': 'Plamen',
        'description': 'Plamen kao kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/plamen.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAADWUlEQVR4nO3XS28bVRjG8f+5zMVz8/gex0njxqbQSt0QVAkWbBBbhISQukGR4KtQIcHn4DtUVVkgdVM2FQKJS5qWElRSIKmd2E4cj89hYYREk0DtJIqQ+i5Hc+b9nefMHJ0RgOUcS55n86kAq/X6+QJCKbler/N+43Qh/wn4+MISABWlqWmNMvDeKSKeK4FP2y1cIXi7ledaKSQ4xVfnuZ7kBw5R5LHQytOqRlzUDh82GmcPuLHURAh49WJEreQTlOClq3lWWikLSrF6CohjAZ80mzhK8tZrNeK8JslJnnZHlBqw3Ap5/ZUiy57DRydEHAvQSnG1nVAoa0qXNG9cT0giSZAailVJvRqw0kxZyHl8cAKEPuriZ+0WUeRQrIbkEks+FPhFydzLDrmSg2DEeCSwmU9mDL2H2cyAIxPI+Zr2fEQaWoK8QAcSxpak6aEaPuGiR/GKJJmT1Gs5ajmX1QuzpXBkAo5WxKlHVLT4JfDLAgIJFQ/qeRAdQgzVy2BGcO1SypNvRzMBDiVw40obL9AkMeRrirDqQaLB1xB4kM9B7IGWRA2HZElRKngUtZ5plzwEkFJyeTmmWJa4NQ2xC5UI6jHEKfghRB4owIPCkiJIYKUd48+wQR1aggNr8BT4qcBJFBQCSFIouhDUIZNQ3J0sya5B+hCWIf1FE0/d/ogE9jODBZQPRBJKEcwVIGjDuAlmDoIE5sO/h4tAEkYuOaVODhiMxggAIcGXUAlBz0FWBetPhpgAFgvgaUwGQSRxA3C1ODlgPzPc/a7DYDACKyEAxgmYeHJ2suKvJMrgeYwzQIH0AecUEri9s0u3N2KvaxkPMhDDSRpWY6zD0JoJzITgOWAUw55hY9vl8Wj6T/EQYL3T4dFwSGfTsLdxAP19EHtYDNZqsArkFsg+/Qf7DLcyeluGh7/tcGd79+QAgPXRAbe+7rBx74D+l1042MDqP7Cij1LboLfhp216Pwzo/Jpx98cxN+//znqnMzXgyJ1wbWePSuDi3usxv+ny5uYatXf2kIUSsMXjL4as3driyTc9HvQH3Pn5Kd93+1M3BxAccyxvpSkA77Zr1DyHwmKZqJJjMBjyaGOHz7+6/4/7Z5n9vwKehTxbszacGnDW9f/5MXkBeAE4q/oTxK3vRXtaptIAAAAASUVORK5CYII=') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAADWUlEQVR4nO3XS28bVRjG8f+5zMVz8/gex0njxqbQSt0QVAkWbBBbhISQukGR4KtQIcHn4DtUVVkgdVM2FQKJS5qWElRSIKmd2E4cj89hYYREk0DtJIqQ+i5Hc+b9nefMHJ0RgOUcS55n86kAq/X6+QJCKbler/N+43Qh/wn4+MISABWlqWmNMvDeKSKeK4FP2y1cIXi7ledaKSQ4xVfnuZ7kBw5R5LHQytOqRlzUDh82GmcPuLHURAh49WJEreQTlOClq3lWWikLSrF6CohjAZ80mzhK8tZrNeK8JslJnnZHlBqw3Ap5/ZUiy57DRydEHAvQSnG1nVAoa0qXNG9cT0giSZAailVJvRqw0kxZyHl8cAKEPuriZ+0WUeRQrIbkEks+FPhFydzLDrmSg2DEeCSwmU9mDL2H2cyAIxPI+Zr2fEQaWoK8QAcSxpak6aEaPuGiR/GKJJmT1Gs5ajmX1QuzpXBkAo5WxKlHVLT4JfDLAgIJFQ/qeRAdQgzVy2BGcO1SypNvRzMBDiVw40obL9AkMeRrirDqQaLB1xB4kM9B7IGWRA2HZElRKngUtZ5plzwEkFJyeTmmWJa4NQ2xC5UI6jHEKfghRB4owIPCkiJIYKUd48+wQR1aggNr8BT4qcBJFBQCSFIouhDUIZNQ3J0sya5B+hCWIf1FE0/d/ogE9jODBZQPRBJKEcwVIGjDuAlmDoIE5sO/h4tAEkYuOaVODhiMxggAIcGXUAlBz0FWBetPhpgAFgvgaUwGQSRxA3C1ODlgPzPc/a7DYDACKyEAxgmYeHJ2suKvJMrgeYwzQIH0AecUEri9s0u3N2KvaxkPMhDDSRpWY6zD0JoJzITgOWAUw55hY9vl8Wj6T/EQYL3T4dFwSGfTsLdxAP19EHtYDNZqsArkFsg+/Qf7DLcyeluGh7/tcGd79+QAgPXRAbe+7rBx74D+l1042MDqP7Cij1LboLfhp216Pwzo/Jpx98cxN+//znqnMzXgyJ1wbWePSuDi3usxv+ny5uYatXf2kIUSsMXjL4as3driyTc9HvQH3Pn5Kd93+1M3BxAccyxvpSkA77Zr1DyHwmKZqJJjMBjyaGOHz7+6/4/7Z5n9vwKehTxbszacGnDW9f/5MXkBeAE4q/oTxK3vRXtaptIAAAAASUVORK5CYII=') 2 2, pointer",
    },
    {
        'value': 'imported_sladoled_rozi',
        'label': 'Rozi sladoled',
        'description': 'Rozi sladoled kao kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/sladoled_rozi.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAE6UlEQVR4nL2X3W8UVRjGn3NmZrttt9giuyXaiiKm0TaRb8INxotiQkks3EgKRGKMV8hfYKIX3njhF4kXgsGQaGqq0UQupCEmpgUaEogfhSAgUii0tNt2v3dmzsf7erGsYNia7rbhTU4ymZPM8zvPc945M2IkfugsgK14uEYARLYmD2+sMLdk5QJA5/PPjgNof1D80uXrD4m3tbW51lohhDATExO8VADl1Zch/iPe3t4u+/r6+nbs2PFWZ2fXWtdz665du3ZzaGjohy+PHfvw4sWL04siGIkf4uy2T8vj7Ej80PnyXEdHR8Pg4OAJYwwba1lpzb4fcC6f51QqzX+Mjk50d3dvWSzA2UriLS0tor+//yutDRMRExEbYzgMQy4UCpzOZDg5M8O//f77VEdHR1ut+hJABBUyX7du3ZZXe3v7AAYRg4jAzOAHkhcQSCRaE/v2739nMQCotOF6enpeA7MgIjw4mAnEDDDAYACM7d3be+sbGupqAXDna7PWlSs7rKUSpSwtu+zEvzDEYGYkWlsTEc9b7gOTVQPMN6GUMtZaMBiSGEIADICIYC3BkoUlAlkCWcvGGKpWHLgXQaUaGxu7oo2BMQbGaJSvrbVgopIbtgRx5erVW0qpdC0AFR1YEY/Lrs6uDUZrEDmQQgBCAACYGUT2vgvWYnh46JdYLKZSqdTSAOzZs+ftjZs2vUxMkCxBzCBmMN/PXQgBKR0wa+zdu+91x3GLn3z80cF8Pl/VG7JiBI7jrgQzbn9zGrcOHMHtXYcxefRnmFCDiHBz4DTOb34P57Z/gPSlcUQiEdGzc+cboVKxah0QlW7WR+qi767ZdXKXfO6lOulAMqBTeczECGGdRP24D0uMvLGYhUK4rc18kR86eObM6SPW2qocqBiBr8KgJStdGyNowZAMcEMdHssG0KGCgoRmW4I1EmbwpjNihwcsqOoDat42TKtiRmkDYxieKwEGKOLACoBCDWvK+wLwoYsE6GrF/xfgrsreCJSBJwQoLLU4McFahpGAdWWpC5hxmacuACguGcAzzuOJ9c5Tvb7SsELCAQBmMDEsMTQRNBEsAMuMAquZOGJNd5HNVAtQsQte8breX+bGnpRPNCO9ysNUq4XyJAJtEGgN4wqMx/MoropAtjRgMz+9ez82n4jCc6oFqOjAn5j+dU1j9spPEydbqTnVvGp5FHGOY339BggrMOIOI9l4F8k84cX6Tdi4+gVOTKnVpmA9ALYagIptKCAEg71EU+SztW1Nb66IRdDc4CEIFbQyaIy6yAUGYzM+bmX1eCYtdzN4Lofw72odqBjBvVNf5QLTL6UAEyFQBk31EaxobkAxNPAVQToSecVfZxGcr0V8XoBy+ZpG0r65YYnhCkBKCYKAUgbGEnwrwlxoj9UivCAAAP5kJvxeOg4a6iNQxpacaIwCUiJZsKeMpZpWvlAATGfD/oKy7GuCMRaeI6AISAcWc745iio3XdUAvqbRZF6N+qFBtM5DxPMwnfGRLNJfuWJ4ajHiCwIAoMbngu+UJWSLGnOFEL4mJAv2OAD/UQBgOhcOzBaMsQzM5UKklChmiuHxxYovGEBbvj6eCs7lQ4vZvMJU3vyojb3zyAAAmMlM8O2dTIhZnzgX2M8B1PQRWnM5Em3tLVG/dVn0AoCa/gEWW3JZ1B2IuPLAUj70Hz2jEyhARM6HAAAAAElFTkSuQmCC') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAE6UlEQVR4nL2X3W8UVRjGn3NmZrttt9giuyXaiiKm0TaRb8INxotiQkks3EgKRGKMV8hfYKIX3njhF4kXgsGQaGqq0UQupCEmpgUaEogfhSAgUii0tNt2v3dmzsf7erGsYNia7rbhTU4ymZPM8zvPc945M2IkfugsgK14uEYARLYmD2+sMLdk5QJA5/PPjgNof1D80uXrD4m3tbW51lohhDATExO8VADl1Zch/iPe3t4u+/r6+nbs2PFWZ2fXWtdz665du3ZzaGjohy+PHfvw4sWL04siGIkf4uy2T8vj7Ej80PnyXEdHR8Pg4OAJYwwba1lpzb4fcC6f51QqzX+Mjk50d3dvWSzA2UriLS0tor+//yutDRMRExEbYzgMQy4UCpzOZDg5M8O//f77VEdHR1ut+hJABBUyX7du3ZZXe3v7AAYRg4jAzOAHkhcQSCRaE/v2739nMQCotOF6enpeA7MgIjw4mAnEDDDAYACM7d3be+sbGupqAXDna7PWlSs7rKUSpSwtu+zEvzDEYGYkWlsTEc9b7gOTVQPMN6GUMtZaMBiSGEIADICIYC3BkoUlAlkCWcvGGKpWHLgXQaUaGxu7oo2BMQbGaJSvrbVgopIbtgRx5erVW0qpdC0AFR1YEY/Lrs6uDUZrEDmQQgBCAACYGUT2vgvWYnh46JdYLKZSqdTSAOzZs+ftjZs2vUxMkCxBzCBmMN/PXQgBKR0wa+zdu+91x3GLn3z80cF8Pl/VG7JiBI7jrgQzbn9zGrcOHMHtXYcxefRnmFCDiHBz4DTOb34P57Z/gPSlcUQiEdGzc+cboVKxah0QlW7WR+qi767ZdXKXfO6lOulAMqBTeczECGGdRP24D0uMvLGYhUK4rc18kR86eObM6SPW2qocqBiBr8KgJStdGyNowZAMcEMdHssG0KGCgoRmW4I1EmbwpjNihwcsqOoDat42TKtiRmkDYxieKwEGKOLACoBCDWvK+wLwoYsE6GrF/xfgrsreCJSBJwQoLLU4McFahpGAdWWpC5hxmacuACguGcAzzuOJ9c5Tvb7SsELCAQBmMDEsMTQRNBEsAMuMAquZOGJNd5HNVAtQsQte8breX+bGnpRPNCO9ysNUq4XyJAJtEGgN4wqMx/MoropAtjRgMz+9ez82n4jCc6oFqOjAn5j+dU1j9spPEydbqTnVvGp5FHGOY339BggrMOIOI9l4F8k84cX6Tdi4+gVOTKnVpmA9ALYagIptKCAEg71EU+SztW1Nb66IRdDc4CEIFbQyaIy6yAUGYzM+bmX1eCYtdzN4Lofw72odqBjBvVNf5QLTL6UAEyFQBk31EaxobkAxNPAVQToSecVfZxGcr0V8XoBy+ZpG0r65YYnhCkBKCYKAUgbGEnwrwlxoj9UivCAAAP5kJvxeOg4a6iNQxpacaIwCUiJZsKeMpZpWvlAATGfD/oKy7GuCMRaeI6AISAcWc745iio3XdUAvqbRZF6N+qFBtM5DxPMwnfGRLNJfuWJ4ajHiCwIAoMbngu+UJWSLGnOFEL4mJAv2OAD/UQBgOhcOzBaMsQzM5UKklChmiuHxxYovGEBbvj6eCs7lQ4vZvMJU3vyojb3zyAAAmMlM8O2dTIhZnzgX2M8B1PQRWnM5Em3tLVG/dVn0AoCa/gEWW3JZ1B2IuPLAUj70Hz2jEyhARM6HAAAAAElFTkSuQmCC') 2 2, pointer",
    },
    {
        'value': 'imported_kriz',
        'label': 'Križ',
        'description': 'Bijeli križ kao kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/kriz.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABzUlEQVR4nMVXMZKDMAxcblxRuXDhB1CkZlLkGXlT3pFn5BEUeQAFD3DhIlUqzXDFnXw2EECGOXaGiQHLWuSV5BQAehwIBQB9/8OhKIpVRjxfYvMJxc96/eqFuq4bPauqKpuAAmRf4b2fvZfiK8eInW51nk3AGJP8/isBYwyUUlBKbXYO/GpACiLaxTkgjMD1ek3uWQPD55sJ9H0/edV1nTiPNdA0DZqmGdksocCgEk7leQzvfdh/5xyAeVF673G5XD6uN9JA27aTCymlkr0nIlhrw3iqPhhjFlN1tAWx89h4SnhEFKLA8zlCa1N0RIBTbLjHHHbvffhidsRz+YpJiQkQEYgoOGcyPGaH1tpEA0Pisd0cRiJcwvP5DBFgR+fzObxfs+8xsgpRHIkhpP1BXIq11kGQh/QC4K8W7NEPxCu8Xi8YY3brB1kRAPY5C2QR0FpDKRWq4FZkbQEAUbGZQ1YEnHOw1h6XBSzCw86EjD10ICbAHQ/Y52gmFiHXf+dcooHhQWbtn5XsLGAijPv9HsZlWeLxeOB0Oi0SERPQWqNt20CCwc+G6LpuloSYQFVVSSecSsX48LoEMYHb7QYAeL/fk+/LskRd16vCDwDfXhL9GJifk2sAAAAASUVORK5CYII=') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABzUlEQVR4nMVXMZKDMAxcblxRuXDhB1CkZlLkGXlT3pFn5BEUeQAFD3DhIlUqzXDFnXw2EECGOXaGiQHLWuSV5BQAehwIBQB9/8OhKIpVRjxfYvMJxc96/eqFuq4bPauqKpuAAmRf4b2fvZfiK8eInW51nk3AGJP8/isBYwyUUlBKbXYO/GpACiLaxTkgjMD1ek3uWQPD55sJ9H0/edV1nTiPNdA0DZqmGdksocCgEk7leQzvfdh/5xyAeVF673G5XD6uN9JA27aTCymlkr0nIlhrw3iqPhhjFlN1tAWx89h4SnhEFKLA8zlCa1N0RIBTbLjHHHbvffhidsRz+YpJiQkQEYgoOGcyPGaH1tpEA0Pisd0cRiJcwvP5DBFgR+fzObxfs+8xsgpRHIkhpP1BXIq11kGQh/QC4K8W7NEPxCu8Xi8YY3brB1kRAPY5C2QR0FpDKRWq4FZkbQEAUbGZQ1YEnHOw1h6XBSzCw86EjD10ICbAHQ/Y52gmFiHXf+dcooHhQWbtn5XsLGAijPv9HsZlWeLxeOB0Oi0SERPQWqNt20CCwc+G6LpuloSYQFVVSSecSsX48LoEMYHb7QYAeL/fk+/LskRd16vCDwDfXhL9GJifk2sAAAAASUVORK5CYII=') 2 2, pointer",
    },
    {
        'value': 'imported_banana2',
        'label': 'Banana 2',
        'description': 'Banana kao kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/banana2.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAE9ElEQVR4nO2UWYwURRzGf1XVx/TM9Mz2zO6wILAiqzxsBDSgiJooajAqeCRqQpRE4wFRYSOSYDwI0ZDwQiSekRcOD6JGBFHjsYqAbowHqLgciyyH3HvNzB6zMz1dPmyAVQ4VdowPfkmnk6ru+n71/etfQm+IaU4jcUVGnG7+bGUA7Pj25AzVY0vqfRwAYNjMtj9MNC3y+tXomuvGmuMvGD4ls6dx46L3v//p6Lg82cdNi7x+3/3+7Yfvfe3NNUtSyejtfcdPAOhr3p/1nzx28IhMawfrv2u65JQApTIH0LmW5LwpSSZdn6yZP3eqewJAKc0BCvHBPww5v4tJd4RDQ6vix9Y34I+nvVRtZ8QSTe2BIiQ7PS8hxgGfAEhxRUb0fUphDnCoecttbsKivFLK6qq9C95aMceBU3RBf2vZK9MvtfxtU0aPqUAMHMW553mj427mzn8NIL1rw7OjU3lzyNByEDVYsRqSCXXbvwLw0bL7Jjrp7ddeOTKKEYkDHuAStoIRJQf4fPV8Sx36akFVuMDwag9EGAKAIr6vgD5XcSmk2n98xMzsGFU5OIKTCoNyIMiB8Ml0yd1QwgTq3q6tCbd8MdezYWC1i4xHwSgDfPI9Odrago0lA/h81ZNusvOL5ZFim1teGSU8vAJiSZAR0FlaWjppbtYfQAlKsHblHDfesfa1WK7xIitiUVZdgSiLgJ0ADQjB7qaOX3K5oL7fAda9N2N4eXfdMi/XMN5KGMTOTWGkysCOgEyA6uHIkQLbt3fPnz7j5UK/Aax97zHTFQfuqSh89Iyr9qfMAQbOsAHIRDkoAVYYRI5CweeH7/UnmbS54ui/Z3X1bnj3/mREZW9MGjseSahdY1SQQ0ZtrEEpiCbBlGDHQETRaDZusg/Vf+OOe/jRF3edMUD9qmnljmy9LKLaJ3uhfTdErbZBpupBF0CEQ8hkEkJRMA2ww6BcdCDY3EDn1/Xxm6fNXFzXd72/BKhf+aBpic5qS/kXh0OtN5XZBydEnWzKNLugGKDzGh0YyFgMEY1AyARD9cZuuKALNGwz8uvWl906vXbph39e/wSAz5ZOVRGneKFrpy+PONnxUTt9UdjJVluhvGmYPggNBU3QLSAwwQohY2GwZW9TGwosB2QU3y+yeYto/ea7AfdMq122+mQbPAbw6ZK7yj21b+pAd//dZV7HyFCsKGVI9xqiQEu0r0ErdFEihAGOjbAUWAqkBiHBcEBYtLQEfLvJWrdzd2r6Q7PfaDhVwgKg7qUJD1xgNzxRmcoONTxFEYNiIFC2QFoKLU0EEpC9B0tqkAKkBDTCDIEZAg2taWjcae9taEwsbMt6L8x6erl/uhIbr86+av6I3IbHkzEDv0OR3gfNR3wqUgJ3qEIkFRgBGLr3DVDUCF+BECAk+Uw3h9Oaxt/sn5v2e4vbuxKvz5r3TuvpjI8lMGOMytVONG0rppAKcl0Qr5C4lRLlKTAFSIGQEmHK3tCEoFDQpDNw8JAqbtsbWb+ntXJhXiQ+nrNgZf7vGB9LoG1AzcIvf93y+KhzinieIhJXKEMT+AGqR0IAPpDP+3QVBO2dRnAk6+w90BLadKA5XJfuSax/6vnPNsG2f+J7PAGAJ2qvvjoVHL5lkNU8PuV2V0UjWklbkJdmIes7B9I5Z0c6F97a2eNs7SpEf84VQjvnPrem44wc/9d/Tb8DfTW65SgHFxgAAAAASUVORK5CYII=') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAE9ElEQVR4nO2UWYwURRzGf1XVx/TM9Mz2zO6wILAiqzxsBDSgiJooajAqeCRqQpRE4wFRYSOSYDwI0ZDwQiSekRcOD6JGBFHjsYqAbowHqLgciyyH3HvNzB6zMz1dPmyAVQ4VdowPfkmnk6ru+n71/etfQm+IaU4jcUVGnG7+bGUA7Pj25AzVY0vqfRwAYNjMtj9MNC3y+tXomuvGmuMvGD4ls6dx46L3v//p6Lg82cdNi7x+3/3+7Yfvfe3NNUtSyejtfcdPAOhr3p/1nzx28IhMawfrv2u65JQApTIH0LmW5LwpSSZdn6yZP3eqewJAKc0BCvHBPww5v4tJd4RDQ6vix9Y34I+nvVRtZ8QSTe2BIiQ7PS8hxgGfAEhxRUb0fUphDnCoecttbsKivFLK6qq9C95aMceBU3RBf2vZK9MvtfxtU0aPqUAMHMW553mj427mzn8NIL1rw7OjU3lzyNByEDVYsRqSCXXbvwLw0bL7Jjrp7ddeOTKKEYkDHuAStoIRJQf4fPV8Sx36akFVuMDwag9EGAKAIr6vgD5XcSmk2n98xMzsGFU5OIKTCoNyIMiB8Ml0yd1QwgTq3q6tCbd8MdezYWC1i4xHwSgDfPI9Odrago0lA/h81ZNusvOL5ZFim1teGSU8vAJiSZAR0FlaWjppbtYfQAlKsHblHDfesfa1WK7xIitiUVZdgSiLgJ0ADQjB7qaOX3K5oL7fAda9N2N4eXfdMi/XMN5KGMTOTWGkysCOgEyA6uHIkQLbt3fPnz7j5UK/Aax97zHTFQfuqSh89Iyr9qfMAQbOsAHIRDkoAVYYRI5CweeH7/UnmbS54ui/Z3X1bnj3/mREZW9MGjseSahdY1SQQ0ZtrEEpiCbBlGDHQETRaDZusg/Vf+OOe/jRF3edMUD9qmnljmy9LKLaJ3uhfTdErbZBpupBF0CEQ8hkEkJRMA2ww6BcdCDY3EDn1/Xxm6fNXFzXd72/BKhf+aBpic5qS/kXh0OtN5XZBydEnWzKNLugGKDzGh0YyFgMEY1AyARD9cZuuKALNGwz8uvWl906vXbph39e/wSAz5ZOVRGneKFrpy+PONnxUTt9UdjJVluhvGmYPggNBU3QLSAwwQohY2GwZW9TGwosB2QU3y+yeYto/ea7AfdMq122+mQbPAbw6ZK7yj21b+pAd//dZV7HyFCsKGVI9xqiQEu0r0ErdFEihAGOjbAUWAqkBiHBcEBYtLQEfLvJWrdzd2r6Q7PfaDhVwgKg7qUJD1xgNzxRmcoONTxFEYNiIFC2QFoKLU0EEpC9B0tqkAKkBDTCDIEZAg2taWjcae9taEwsbMt6L8x6erl/uhIbr86+av6I3IbHkzEDv0OR3gfNR3wqUgJ3qEIkFRgBGLr3DVDUCF+BECAk+Uw3h9Oaxt/sn5v2e4vbuxKvz5r3TuvpjI8lMGOMytVONG0rppAKcl0Qr5C4lRLlKTAFSIGQEmHK3tCEoFDQpDNw8JAqbtsbWb+ntXJhXiQ+nrNgZf7vGB9LoG1AzcIvf93y+KhzinieIhJXKEMT+AGqR0IAPpDP+3QVBO2dRnAk6+w90BLadKA5XJfuSax/6vnPNsG2f+J7PAGAJ2qvvjoVHL5lkNU8PuV2V0UjWklbkJdmIes7B9I5Z0c6F97a2eNs7SpEf84VQjvnPrem44wc/9d/Tb8DfTW65SgHFxgAAAAASUVORK5CYII=') 2 2, pointer",
    },
    {
        'value': 'imported_duga2',
        'label': 'Duga 2',
        'description': 'Šarena duga kao kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/duga2.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAE+klEQVR4nL2XTWgbVxSFP4UXeAMJzIADGpDBU1LomG4k6MIGL6qu4tBFbdJFDF1EECgxXTShi2C8KCKLELxI8wNt3UCLuinWJsSLlqoLg7IIyAUHTRfBY0hhDA7MgwrmQQami5Esjfwb8nM3o7l6uue8c89cvQFgc6OZNBu1JAw2E95x5FqPV5KV76+hdYidd3E/Ok/5s6sYhpF7FwSEDsMUfKxE+G+bxm9VtA6JojAxDOutkxDpRVIxishCEd1RVP+ooZWivf5nMl785K2SONH7YIYgNZjCpFqYpb3RoH5vnubqnbfqDbFfUsaS6sg0nghY/mUBZ61O4LcS2ym9cTVO7J/WcDrAdRVXpmy8p01qSxWaq3eS6L/wjaqxPwGpoeCDaOOYmuoFB601Kw8WqN2/QhS+ORJ7WyA0jAYgVTcRYUq4esnE27GoPaizrBWtRi0pTl0kdzL3Wm0ZIqDBDsD0gai/wpHIMU3xLDiuQ/WbBr7XIlQBycskeR0SWQIyhBEfCAfALSiQ5gSYZsStezbeVkTt3i20Dl/LoH0PCA2jCoTqg492wUXYpypAC9AfGkwuGTQe3mV5qUL7yaMkil7dG30Ctp+VXhpQMLPggAY8GdGSEd5IhPuTRaQClpcq1O9fIdwJXolEv/SIR6bvo2ZqxCGX+AJaElQ3r2SE9TOgbZoX64ThNmGwmVj2e8dqyUALBk1nQUGz64VuKMAbAN+N2EZ3ZjFv1vD+blL7YZ7geftYSmTnQK/vY9AzXS804AtjiBKAhVbTRC8qoGcwbz7Ce7JK7XaF5u8/JsnL6FAiWQLSSvu+B9zCE1ZG+v6XNlHnPMT59D4uYd5oEWx51O7Ps/xd5dDBNdACA9630ymYATHwhaYlQ1SvTb2IbXSnDNrpJhSpVi5yMUQKibdWZ32tdrQCelTCSAAiyCxQpK7ft+9qNpU+zndXSiDfvUJpYhqEPOAvb4iAHNtrOo2BLyAQxhHgdEFlZlkQ+FgjNqbtHkigz01EQ3038ERES6ai9mPAdLvgeghco2/Y6FM2018scNihZsCE/V1q2AVXQ36Q2smaDpWtGCv0ooWUkvKFBUpTc4fOg4Hy0QA4+zpexg5qj+kAJMQK9a0NMdhjLtOfL1Camj1yGGUew4PBDSQOWpWJXsx1d99rjIkRK8Z9H2IwR2xmLt06FniGgBKwLqAljQy4xMIkD9omVOWs6WITQ4Hrg/vUZe6DFkoF+BsNkpfJsSbhLlRDGgQSNIPPugFIdGyg1CTEEtgG8qDBea4Z35KYoQkxSOEipaT516/YTuk4+H0FAjHs9q6vY4l6Vib8qoq6Pom6bmPobcZ9TekfibkDxP3fzJ31UCqguXqXo8YwgIhiDbEGbSFP6QESBmznCRa3US+qOAUX2ynRXn9EdLuIO+Yj4/1KSqSQaB1liB2sQJeA+roPLDsW4WXwLj9Gd0KKEzNUFleY+fIOk5/OozuKsOPvKaZYp/bMQcca2xlPp+BRCpSm5vCftVhfqxNeNJHSQOsAKS0mP64wca6Cc7ZI7mT6rtgzV+Nhmdm8hxQmKt5mZcuBGKyCy8TUHJPnKsc6sArrjJ0Ld4LEMm2C5x7ytElpYha74JIvOLvAvcidzOWiKErUtk9tzUltHINdKFKcmqU0MUN6GLl25O4BMsV7uzsO8zDYTLyNRuofYeEWy1hn7Fc+mP4PEkM+yCoXXbYAAAAASUVORK5CYII=') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAE+klEQVR4nL2XTWgbVxSFP4UXeAMJzIADGpDBU1LomG4k6MIGL6qu4tBFbdJFDF1EECgxXTShi2C8KCKLELxI8wNt3UCLuinWJsSLlqoLg7IIyAUHTRfBY0hhDA7MgwrmQQami5Esjfwb8nM3o7l6uue8c89cvQFgc6OZNBu1JAw2E95x5FqPV5KV76+hdYidd3E/Ok/5s6sYhpF7FwSEDsMUfKxE+G+bxm9VtA6JojAxDOutkxDpRVIxishCEd1RVP+ooZWivf5nMl785K2SONH7YIYgNZjCpFqYpb3RoH5vnubqnbfqDbFfUsaS6sg0nghY/mUBZ61O4LcS2ym9cTVO7J/WcDrAdRVXpmy8p01qSxWaq3eS6L/wjaqxPwGpoeCDaOOYmuoFB601Kw8WqN2/QhS+ORJ7WyA0jAYgVTcRYUq4esnE27GoPaizrBWtRi0pTl0kdzL3Wm0ZIqDBDsD0gai/wpHIMU3xLDiuQ/WbBr7XIlQBycskeR0SWQIyhBEfCAfALSiQ5gSYZsStezbeVkTt3i20Dl/LoH0PCA2jCoTqg492wUXYpypAC9AfGkwuGTQe3mV5qUL7yaMkil7dG30Ctp+VXhpQMLPggAY8GdGSEd5IhPuTRaQClpcq1O9fIdwJXolEv/SIR6bvo2ZqxCGX+AJaElQ3r2SE9TOgbZoX64ThNmGwmVj2e8dqyUALBk1nQUGz64VuKMAbAN+N2EZ3ZjFv1vD+blL7YZ7geftYSmTnQK/vY9AzXS804AtjiBKAhVbTRC8qoGcwbz7Ce7JK7XaF5u8/JsnL6FAiWQLSSvu+B9zCE1ZG+v6XNlHnPMT59D4uYd5oEWx51O7Ps/xd5dDBNdACA9630ymYATHwhaYlQ1SvTb2IbXSnDNrpJhSpVi5yMUQKibdWZ32tdrQCelTCSAAiyCxQpK7ft+9qNpU+zndXSiDfvUJpYhqEPOAvb4iAHNtrOo2BLyAQxhHgdEFlZlkQ+FgjNqbtHkigz01EQ3038ERES6ai9mPAdLvgeghco2/Y6FM2018scNihZsCE/V1q2AVXQ36Q2smaDpWtGCv0ooWUkvKFBUpTc4fOg4Hy0QA4+zpexg5qj+kAJMQK9a0NMdhjLtOfL1Camj1yGGUew4PBDSQOWpWJXsx1d99rjIkRK8Z9H2IwR2xmLt06FniGgBKwLqAljQy4xMIkD9omVOWs6WITQ4Hrg/vUZe6DFkoF+BsNkpfJsSbhLlRDGgQSNIPPugFIdGyg1CTEEtgG8qDBea4Z35KYoQkxSOEipaT516/YTuk4+H0FAjHs9q6vY4l6Vib8qoq6Pom6bmPobcZ9TekfibkDxP3fzJ31UCqguXqXo8YwgIhiDbEGbSFP6QESBmznCRa3US+qOAUX2ynRXn9EdLuIO+Yj4/1KSqSQaB1liB2sQJeA+roPLDsW4WXwLj9Gd0KKEzNUFleY+fIOk5/OozuKsOPvKaZYp/bMQcca2xlPp+BRCpSm5vCftVhfqxNeNJHSQOsAKS0mP64wca6Cc7ZI7mT6rtgzV+Nhmdm8hxQmKt5mZcuBGKyCy8TUHJPnKsc6sArrjJ0Ld4LEMm2C5x7ytElpYha74JIvOLvAvcidzOWiKErUtk9tzUltHINdKFKcmqU0MUN6GLl25O4BMsV7uzsO8zDYTLyNRuofYeEWy1hn7Fc+mP4PEkM+yCoXXbYAAAAASUVORK5CYII=') 2 2, pointer",
    },
    {
        'value': 'imported_kriz2',
        'label': 'Križ 2',
        'description': 'Bijeli križ kao kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/kriz2.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABzUlEQVR4nMVXMZKDMAxcblxRuXDhB1CkZlLkGXlT3pFn5BEUeQAFD3DhIlUqzXDFnXw2EECGOXaGiQHLWuSV5BQAehwIBQB9/8OhKIpVRjxfYvMJxc96/eqFuq4bPauqKpuAAmRf4b2fvZfiK8eInW51nk3AGJP8/isBYwyUUlBKbXYO/GpACiLaxTkgjMD1ek3uWQPD55sJ9H0/edV1nTiPNdA0DZqmGdksocCgEk7leQzvfdh/5xyAeVF673G5XD6uN9JA27aTCymlkr0nIlhrw3iqPhhjFlN1tAWx89h4SnhEFKLA8zlCa1N0RIBTbLjHHHbvffhidsRz+YpJiQkQEYgoOGcyPGaH1tpEA0Pisd0cRiJcwvP5DBFgR+fzObxfs+8xsgpRHIkhpP1BXIq11kGQh/QC4K8W7NEPxCu8Xi8YY3brB1kRAPY5C2QR0FpDKRWq4FZkbQEAUbGZQ1YEnHOw1h6XBSzCw86EjD10ICbAHQ/Y52gmFiHXf+dcooHhQWbtn5XsLGAijPv9HsZlWeLxeOB0Oi0SERPQWqNt20CCwc+G6LpuloSYQFVVSSecSsX48LoEMYHb7QYAeL/fk+/LskRd16vCDwDfXhL9GJifk2sAAAAASUVORK5CYII=') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABzUlEQVR4nMVXMZKDMAxcblxRuXDhB1CkZlLkGXlT3pFn5BEUeQAFD3DhIlUqzXDFnXw2EECGOXaGiQHLWuSV5BQAehwIBQB9/8OhKIpVRjxfYvMJxc96/eqFuq4bPauqKpuAAmRf4b2fvZfiK8eInW51nk3AGJP8/isBYwyUUlBKbXYO/GpACiLaxTkgjMD1ek3uWQPD55sJ9H0/edV1nTiPNdA0DZqmGdksocCgEk7leQzvfdh/5xyAeVF673G5XD6uN9JA27aTCymlkr0nIlhrw3iqPhhjFlN1tAWx89h4SnhEFKLA8zlCa1N0RIBTbLjHHHbvffhidsRz+YpJiQkQEYgoOGcyPGaH1tpEA0Pisd0cRiJcwvP5DBFgR+fzObxfs+8xsgpRHIkhpP1BXIq11kGQh/QC4K8W7NEPxCu8Xi8YY3brB1kRAPY5C2QR0FpDKRWq4FZkbQEAUbGZQ1YEnHOw1h6XBSzCw86EjD10ICbAHQ/Y52gmFiHXf+dcooHhQWbtn5XsLGAijPv9HsZlWeLxeOB0Oi0SERPQWqNt20CCwc+G6LpuloSYQFVVSSecSsX48LoEMYHb7QYAeL/fk+/LskRd16vCDwDfXhL9GJifk2sAAAAASUVORK5CYII=') 2 2, pointer",
    },
    {
        'value': 'imported_list2',
        'label': 'List 2',
        'description': 'Zeleni list kao kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/list2.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAo0lEQVR4nO2WsQ2AIBBFv8aF3MNdHMElHMUJHMDKlsTKjsLaQisaE+VzgiTmfg/v3YX8UAA4kDFlTrgKqMD/BAbTop/qoDNVDKjLso2w6/6NgAMv2yi9QiYQCywSGEz7CLbrjq6ZgwToR+iDS0MJpILTAkwk66cEUk5PCTCRTg+8LCJXOlK4V+Bu/THAlEBKMCVw7faYYJcC+ilVARVQARXInBPpIk7UXAHeCQAAAABJRU5ErkJggg==') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAo0lEQVR4nO2WsQ2AIBBFv8aF3MNdHMElHMUJHMDKlsTKjsLaQisaE+VzgiTmfg/v3YX8UAA4kDFlTrgKqMD/BAbTop/qoDNVDKjLso2w6/6NgAMv2yi9QiYQCywSGEz7CLbrjq6ZgwToR+iDS0MJpILTAkwk66cEUk5PCTCRTg+8LCJXOlK4V+Bu/THAlEBKMCVw7faYYJcC+ilVARVQARXInBPpIk7UXAHeCQAAAABJRU5ErkJggg==') 2 2, pointer",
    },
    {
        'value': 'imported_macija_sapa',
        'label': 'Mačja šapa',
        'description': 'Mačja šapa kao kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/macija_sapa.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABW0lEQVR4nMWW4a2EIBCEh8t1hK3YAleLJUgJtmALS03cj/fwlhUUOfAmMTFowufsLKsC4PFDPcMNEQEApmkCACzLAqXULRA+pXEct3v8udTrgl/X9ZcQ8UIOpiMEPBF5Ito2uRPikQgErLWprGzPW8tDuHAqmvs54Jw7R9YGnuavvxwANoBhGCKIEpAWEJEDHCKA9IbYlaAYQpsmEAoHsyAczwCgtd6/4OJuUcPrMsDOAS6Zi52YC0CdE4cOBHEnAOFGcEHAlA6yIoAshEscWAykBKIYIAkBVhbhQCnEJYAsRGbzEpDLAAAwm7gjjDHVEIddkNPLJjrC2XQmmFKDrApAQkTT8yJENcAhxIk4RFUGpGozAWe/c6CFmgDIUDro80n6n5XmDmjzmQfhv4LDSLAmGeCSB5WUs/HEbA6Qg5AbB90SwtzmtwHwXEh1KUGQLEXKiedupYOOSvAGkyeucgh4ux0AAAAASUVORK5CYII=') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABW0lEQVR4nMWW4a2EIBCEh8t1hK3YAleLJUgJtmALS03cj/fwlhUUOfAmMTFowufsLKsC4PFDPcMNEQEApmkCACzLAqXULRA+pXEct3v8udTrgl/X9ZcQ8UIOpiMEPBF5Ito2uRPikQgErLWprGzPW8tDuHAqmvs54Jw7R9YGnuavvxwANoBhGCKIEpAWEJEDHCKA9IbYlaAYQpsmEAoHsyAczwCgtd6/4OJuUcPrMsDOAS6Zi52YC0CdE4cOBHEnAOFGcEHAlA6yIoAshEscWAykBKIYIAkBVhbhQCnEJYAsRGbzEpDLAAAwm7gjjDHVEIddkNPLJjrC2XQmmFKDrApAQkTT8yJENcAhxIk4RFUGpGozAWe/c6CFmgDIUDro80n6n5XmDmjzmQfhv4LDSLAmGeCSB5WUs/HEbA6Qg5AbB90SwtzmtwHwXEh1KUGQLEXKiedupYOOSvAGkyeucgh4ux0AAAAASUVORK5CYII=') 2 2, pointer",
    },
    {
        'value': 'imported_macka2',
        'label': 'Mačka 2',
        'description': 'Bijela mačka kao kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/macka2.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAB+klEQVR4nLVXwW3rMAx9Dv4GPwMEyAgqoA2YAbpBD84WPviQDXrIEB0gmSACOoIDdIB0BvXQ0p+yTFmSfx9gRJapvEeKpGwA8LUXEa1eswEA7z1qQUSrbDc8qBVxet4tiiAiEBFOz7vo2R95471H0zRFAowxOH3TYPd5nbVpf4iNMcDbR/BsMzWuiYQxJvDOGBP8TsdJAVUiTAvTnnF+j9ed3z1Me04u9xIozOhSzFYBgHHvS70/Pn2vOzYNjpP8kXPHp2a0ldhI8hpoeztn9/GXcL3GiVrdhG63W9E2KI2rnpwhx957307yim1WCyCiiFwTIecT5D5oRBq40/V9DwCw1kY21lo457LnGUkBOcRTslKoAogomziF+/1eLoDJ1xDnYrYVS2gNJAdL3s8KkN5L4loR+/2+TMD/AnvvnEPXdbMdMBIw3Xt5us2ddFqIeX7Je2ChDDViDVJQDjkj6HStwXgtYRiG4CzgjsddMdUB+UrmwJoKyMWvJWG1gJfXW3BfkgO1UI/Zpf0fhiF6J5B5kJMDQRVwrWpteFp2j8djtfdqGTrnsN1uo3lJ2nVd8s+tteOBpjWiSIA05MUSkvRyuYzjw+EQ3EsRKcxGQFPLpPyCwW1WE8pbmYpCg5/3slykvgM5AiwM+BdF7TwoFpArru/7YLu0qH4BZhSYjj5w5ioAAAAASUVORK5CYII=') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAB+klEQVR4nLVXwW3rMAx9Dv4GPwMEyAgqoA2YAbpBD84WPviQDXrIEB0gmSACOoIDdIB0BvXQ0p+yTFmSfx9gRJapvEeKpGwA8LUXEa1eswEA7z1qQUSrbDc8qBVxet4tiiAiEBFOz7vo2R95471H0zRFAowxOH3TYPd5nbVpf4iNMcDbR/BsMzWuiYQxJvDOGBP8TsdJAVUiTAvTnnF+j9ed3z1Me04u9xIozOhSzFYBgHHvS70/Pn2vOzYNjpP8kXPHp2a0ldhI8hpoeztn9/GXcL3GiVrdhG63W9E2KI2rnpwhx957307yim1WCyCiiFwTIecT5D5oRBq40/V9DwCw1kY21lo457LnGUkBOcRTslKoAogomziF+/1eLoDJ1xDnYrYVS2gNJAdL3s8KkN5L4loR+/2+TMD/AnvvnEPXdbMdMBIw3Xt5us2ddFqIeX7Je2ChDDViDVJQDjkj6HStwXgtYRiG4CzgjsddMdUB+UrmwJoKyMWvJWG1gJfXW3BfkgO1UI/Zpf0fhiF6J5B5kJMDQRVwrWpteFp2j8djtfdqGTrnsN1uo3lJ2nVd8s+tteOBpjWiSIA05MUSkvRyuYzjw+EQ3EsRKcxGQFPLpPyCwW1WE8pbmYpCg5/3slykvgM5AiwM+BdF7TwoFpArru/7YLu0qH4BZhSYjj5w5ioAAAAASUVORK5CYII=') 2 2, pointer",
    },
    {
        'value': 'imported_morski_pas',
        'label': 'Morski pas',
        'description': 'Morski pas kao kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/morski_pas.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAADPElEQVR4nMWWMWgbVxjHf6ecQ1Wbg7gZ3h3YuKmqxekgG2QKxVo6eXO7eMjQJQRuMCZjucUiSzwI4UFg6no2hrabO7VotF2QunS5qrSNw/MR40AOuwZLzssg7qyzdIl9ktMPHry77+6+3/2/9773aYDifzQdwCmt0dSHATj8/Vc2NjbeG4AGqGq1ylHaYm93L3QMtU5wd35ha2vr5gGklLiuy1HaCh2/7ewAoJ+f8uTxo5sFAJBS4nkefzdHAPh6Jovrumz8vIN+for/zx+srq4OHCAVTCzLQgjBR6cydGazWZSWonUrjTExyeLi4sABQgUAZmdnASgWixylLc6bZ7w69AD465mMKGEYBr7vDw6gVqshhABgaWkJ27Z5od/l1tBtAF7KZxGIRqPBN9+uRD726tDj4fyXyQACiFwux8HBQRfEcKrF/nPZBTH/8DEAjX2Pp4sPrq1AqvNiamqKer0OgG3bVCoVMh+ecd484+S1zqg1zifjFk19GGNikkwmw0/flWjse2jq9bWDdykQWJAO13XDXF9OR2PfY6h1Eiqxvb2dCCDV66bjOHieRzabRQiBYRihEgCj1jiZMRFWz6TBuwCklEh5sQ1N0wRACIHv+3xxbzTycmZMkM7kEwePAHQGXl9fx3GcCESlUgGIqDBqjQP0VR/0YGJZVpezXq+Ty+UwTRPbtllYWGBzczNSMTNjgn9bk4kBeq6BwDp3RaFQANqKBPUC2ko09eHEKrwV4DJEsVgMQT4eOg6fyc/kMSaSqfBOgABC0zQMwwAuVOiESKrClQA6QcrlMoVCIVycAUR+Jp9oR1wLIIA4Pm4HDQ6j75eXQv/ySvlmAaBdKaenp8P1APDZnbYK/31w91oQ+rsfiYeACxWEEIyMHAP5SGt3FVP9DKWUqtVqam5uTvm+r6SU6oddVy2vlK/0fqIUxJlhGJimyVf5T7lfmHtrKpzSWjjvSwHaXXVPZQI1Lvuc0lrn/f4BlFI9IQKfU1rrCi6lVIDq2Q8kMaUUmqbF+n7c+xOAz8faZ0jn2dO3Ap1/G+cL/vjyGOgijFMAwHXdWN/AFIgb1Wo1VoHEheiqFjQ6vfoNiGlK36e9ASsECgq3E/t0AAAAAElFTkSuQmCC') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAADPElEQVR4nMWWMWgbVxjHf6ecQ1Wbg7gZ3h3YuKmqxekgG2QKxVo6eXO7eMjQJQRuMCZjucUiSzwI4UFg6no2hrabO7VotF2QunS5qrSNw/MR40AOuwZLzssg7qyzdIl9ktMPHry77+6+3/2/9773aYDifzQdwCmt0dSHATj8/Vc2NjbeG4AGqGq1ylHaYm93L3QMtU5wd35ha2vr5gGklLiuy1HaCh2/7ewAoJ+f8uTxo5sFAJBS4nkefzdHAPh6Jovrumz8vIN+for/zx+srq4OHCAVTCzLQgjBR6cydGazWZSWonUrjTExyeLi4sABQgUAZmdnASgWixylLc6bZ7w69AD465mMKGEYBr7vDw6gVqshhABgaWkJ27Z5od/l1tBtAF7KZxGIRqPBN9+uRD726tDj4fyXyQACiFwux8HBQRfEcKrF/nPZBTH/8DEAjX2Pp4sPrq1AqvNiamqKer0OgG3bVCoVMh+ecd484+S1zqg1zifjFk19GGNikkwmw0/flWjse2jq9bWDdykQWJAO13XDXF9OR2PfY6h1Eiqxvb2dCCDV66bjOHieRzabRQiBYRihEgCj1jiZMRFWz6TBuwCklEh5sQ1N0wRACIHv+3xxbzTycmZMkM7kEwePAHQGXl9fx3GcCESlUgGIqDBqjQP0VR/0YGJZVpezXq+Ty+UwTRPbtllYWGBzczNSMTNjgn9bk4kBeq6BwDp3RaFQANqKBPUC2ko09eHEKrwV4DJEsVgMQT4eOg6fyc/kMSaSqfBOgABC0zQMwwAuVOiESKrClQA6QcrlMoVCIVycAUR+Jp9oR1wLIIA4Pm4HDQ6j75eXQv/ySvlmAaBdKaenp8P1APDZnbYK/31w91oQ+rsfiYeACxWEEIyMHAP5SGt3FVP9DKWUqtVqam5uTvm+r6SU6oddVy2vlK/0fqIUxJlhGJimyVf5T7lfmHtrKpzSWjjvSwHaXXVPZQI1Lvuc0lrn/f4BlFI9IQKfU1rrCi6lVIDq2Q8kMaUUmqbF+n7c+xOAz8faZ0jn2dO3Ap1/G+cL/vjyGOgijFMAwHXdWN/AFIgb1Wo1VoHEheiqFjQ6vfoNiGlK36e9ASsECgq3E/t0AAAAAElFTkSuQmCC') 2 2, pointer",
    },
    {
        'value': 'imported_morski_pas2',
        'label': 'Morski pas 2',
        'description': 'Morski pas kao kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/morski_pas2.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,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') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAHOklEQVR4nMXUaXBT1xUH8P+9T8/aLcmSLONFtjEYsZjVEAq0kBATlklCgTKZpoA7aSAzhBhKk0wYSEkYCgydFNqa0BBSCtRxIW2HpSwmISYZSMLihYBtZATIq2RZsqz1Pcm6rx+CGdqASzqY/D/deWfmvN+cc+eSmopW+8Wz9YqzH1VtyR5r2bd+35IAHmGorzOgSx9qziqYm7/Ned29d8mITVMeKeDLA3V7knVaZGamcRNmFzybNWnAiZ8Oe3vNqqd2mB8JQAxHDiCCDpPFQFKMKcjNs6pHzBqyMSAE/7X6mdLp/Q5Izddca6ruOG+y6KFU86yjy4lwxCcNHp87Pp7E9i0YtO71DUs/SOo3wPLSH4disWC5TqsVw0In2fXhRjCVTzKa9FJ2XuYA28y8zfXVzRXrFr2X2S8AALh62nHC3x7syB5oJS8sXoE5RfOg1WoljVrNtLwOueOsUxvtreXPZrw2+mEDSO/h/ZJP/zD7l9NeDnV0o6uzG93dUXi9neihAfSE5bhub0anq7PNfy3wcuGcEYdffWdh4mEAaO8h7nGU1e7am3AFBRiMOpaWZmI3Or5kK9Y8D71VZGajSUq3ZqSnjU0tu/qFfc2WleXyhwqYOG+YfaLSXe97rxR+Xk6S9Wpizc5AxB9HslYLpVqB5CQVM5tMCsMgw9or5+3bHgbgzgpqD1WT4c+MnsFt3rjldB0bZV61mqXqePCKBHU0eJj96yZoFHLcaGylIVGQovEgEZyJk4WFBU1ai2JYIBDWdXeGArcuumrjCqEiTmIVpRUrIw8M6E08wZ4MFS870lg4T2EqehIxfwTBYBjd3iAkTsS5j2tgNqfCG+iCJlkFrV6FnngC8VgPGICYIKLLG4g5Ltz6q0qneP3Pn73heSBAT7t7Fafkq5vqvfXWwdqi1jf/uD2w5DWDr8lDgpEAU2o4HDx0GOqeFPrY5ELmuNmMmBiHJEkUEmEMCdIV6CJul9svRkQ/kUMbaApVGFOMy8rPbwjeDyADAM/O8tGxj46uExIyuV4hawy1aCtTh6dfT9RdGKeb/gRX/9lVHDt8mrgcndIvls7CpaqrSDGYSYQKkhARAQpEwiHS7Gx26pL0y0iMfE3BZfZo2cLGqpsFAM71CbDL8sfaZudrhAh4JgqjEu7uUbKAPKpqv0EY9wRybdl4PP4jKX9oLo6cOoamRjeWFC+WbjmdSFARPFEiIkThve7f+fe2LSdv92579bmdtWlplqRLx/f3vYKyksNm26zxF9LzTNmxWAKEo6BKHpwcYH4BCQZwVIabdifOfv4V8vLyoEvR41JVFYpmTkGbM4jKTz+H87qzZsTwYTN//adF7r72fs878NbcsnXFm+e+zTEOjDEmSex2mVCJMEZBwfM8OI6joWCIeTr8cLf5MHBQJr1cbWdNN1uIx+8h9kuOvRMmjVm+bufPQg8CuPMOFM3N/d3R3Z/8s9PfBQJCKKWEEAJCADCAMUZEUYQgCJBxHExmHcm0mtHS3A5CJKSY9Eg1WqSMIZbFJ/9R+eaDTuAOYFLxD0I2W+orJz+sPNTW4SZirAeEfDMgSikASHfGxnEIhMJSu8uNFKMeRrMeao1KisT80g+nj8WCl55ePcO6YtZ3AgDA9Bceaxk/uWDxu2/t3/XFuaqwx+ujkiSBEEI5jqP0toTjCL1SU09VahXVJqthMOqoRqekBn0KnTCuENOmT6SKNPnW1fNLh/4vwLceot6UPL19MhRkTeHUkVMH23LURoNekiclSeQbBItGRPAyHlRGqCgILNAVQldXBAaDltrrnexy3RV64ePqY0Py8p7bUbH6P96BLcUHTZFodEBKmrbxvgAA2LX+hN5xzTnN5e5cVLRw8ryMrHSkmo3QqJSSTCZDIsEkQghNJBiLRgQSCkSkhvobNCbEmBCJkWsOO2pP1f+q0rXzHQA4vLVqQByJpeCkoj2/PVg+coptd5+Au1OUuSJ/5CTbTxR6+YJcW1ZO7sAsvSXNDJVCAZ6XMY6jcLV5cfFiNbXZhrL2lg54PF5aU3s5HHII80veKDbFFPEd4WiYnvjLmRd/f2JleZ8ruF/WLt5tslhNE2q/qns8LdcyY8jI3BHZg7KoPjkZCj4J0VAMfJIMLc0u+H1BtLa2S0Qk7VmDLQaNQZU4vrdyxbajr+zp7fedAb05UHqW8nLeWHHgzCAhLs4fWJDzVMZAS06GNV2lUigpkQjCwajU7QsRn88L6+B0nD9etWn9np+vubvP/w347/zmpTLqaGgao9IrisSYOCFnWNYYc4bJatQZqCiIQIJ5j+w5nVl2ab3QL4C7s/b5D1Qakyqvpc41euLMcVsNmcmWiv2V728/UvJif/yvz7y7/NSmYwerpTk5JYvuVaf3+vgwU3O84W9BX4jFIj2+7wWQOlHb0HDm1ie8Uqb4XgAbyoqFWw2tpYk4U92rLutvAADo0zUVSWqrGm3frv0bUyEhIB0W3g8AAAAASUVORK5CYII=') 2 2, pointer",
    },
    {
        'value': 'imported_neon',
        'label': 'Neon',
        'description': 'Neon kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/neon.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAADoUlEQVR4nMXXz2ucRRzH8ffM8+xuknXdJNtsSpDSk5QeLEYEEc968uBZQVFBi6YJDaX1IlLwJjZWECsxSkE96Ek8VRREKCkF/SfUNrvN/uj+fJ758fWwz6LtszVLk60DA8szMJ8XM888O18FcHjLLwBzQB7IMWgR0AHqN1/VVSbU1OEtXwQWgXKCyCZjMVAHKpNE6CQwn4QvAo8kfTF5VgbmklWaCCCX9CyQDy88vdHdfGkjQU0coe9+ECwd4+j6ZcyvXz4QRArQaBuOH9csvfAy/StbE0ekAOI9R7LCoWOK0nOv0P7+0kQRaYATfusIb5ehcFRReOY1mt9enBgiDUDRui2cyEFhUZErK2aeepPG1x9MBJEGCMQdz2YDXlxQZAqaYE4x/eQK9a/eP3BECoD3+K7jagMUkMsqMlOaoCTklk9Ru3z+QBEjABBHHtOEb24JYagIw4BgKiScF7LLK9S+eOfAEOkt0IKNPCbyRC2FiYEA9FRAkM8QFh2Z5XV2t84eCCIF8M5hohhjhH4PbARiB9sRTOcIilPohw2Zx0+zu3V634gRWyC4yGIceAvWgPMgXoHWBMUZwkMP4QsR+sQZqpur+0KMOIYWawwu9oNwC94PRlBAqNGlPMHSLKZkCZ44R+XSqftGpADKemJj6RswDpwTEBA1QIiAKE1QKqCPlDElTbB8lsqnK/eFSAGceEzfE3khjgTrwHqFNQpjFKansB2FaWuEHGp+FrswQ/DYGSqfvHUvRHFsAOIxXogt9ARiAzYWTCxEHU/UMERNS1yzcMtA06FMiJ0uoh9dp/LRybsRef655KRamMpHIBLakWfaC9IH2/K4Tg9bq5GxgA4IgwAIwHrEgfgAkVlU6Xl2zj+7sfjulbUkeHjfGA/gnQcLs6Gi0QVagm8YXLVOqXKN2o0fIa6BVoOXUvzgLXUxOA22h+r/ea+8vQEA4jTVpkK1FNQM0mgzv3ONeneb8upna2PO3WFwr4ySPi5AwGpoBVAVZLfP3M429dZVyq9/uJZMXB8DMLzUDiHjAcQL0tdwE6Tap1C9TqPxE+U3LgzDd5KJ7R6Af1/rm2MDEA+9ANox05XrtG//QPlkKrwCdMcAxP8VPhrgQDqebP13+s3vKK9cHBV+YHXCiBUwyF+/YPvblFc/nmj4SIDu/oG98TmL7/088XAYlGYL3FkN5ZOxiYfDYAVi7jxaD7Q2VPA/V8fDH8k/1vDbPQTseYz22/4GrvgB8OktBhwAAAAASUVORK5CYII=') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAADoUlEQVR4nMXXz2ucRRzH8ffM8+xuknXdJNtsSpDSk5QeLEYEEc968uBZQVFBi6YJDaX1IlLwJjZWECsxSkE96Ek8VRREKCkF/SfUNrvN/uj+fJ758fWwz6LtszVLk60DA8szMJ8XM888O18FcHjLLwBzQB7IMWgR0AHqN1/VVSbU1OEtXwQWgXKCyCZjMVAHKpNE6CQwn4QvAo8kfTF5VgbmklWaCCCX9CyQDy88vdHdfGkjQU0coe9+ECwd4+j6ZcyvXz4QRArQaBuOH9csvfAy/StbE0ekAOI9R7LCoWOK0nOv0P7+0kQRaYATfusIb5ehcFRReOY1mt9enBgiDUDRui2cyEFhUZErK2aeepPG1x9MBJEGCMQdz2YDXlxQZAqaYE4x/eQK9a/eP3BECoD3+K7jagMUkMsqMlOaoCTklk9Ru3z+QBEjABBHHtOEb24JYagIw4BgKiScF7LLK9S+eOfAEOkt0IKNPCbyRC2FiYEA9FRAkM8QFh2Z5XV2t84eCCIF8M5hohhjhH4PbARiB9sRTOcIilPohw2Zx0+zu3V634gRWyC4yGIceAvWgPMgXoHWBMUZwkMP4QsR+sQZqpur+0KMOIYWawwu9oNwC94PRlBAqNGlPMHSLKZkCZ44R+XSqftGpADKemJj6RswDpwTEBA1QIiAKE1QKqCPlDElTbB8lsqnK/eFSAGceEzfE3khjgTrwHqFNQpjFKansB2FaWuEHGp+FrswQ/DYGSqfvHUvRHFsAOIxXogt9ARiAzYWTCxEHU/UMERNS1yzcMtA06FMiJ0uoh9dp/LRybsRef655KRamMpHIBLakWfaC9IH2/K4Tg9bq5GxgA4IgwAIwHrEgfgAkVlU6Xl2zj+7sfjulbUkeHjfGA/gnQcLs6Gi0QVagm8YXLVOqXKN2o0fIa6BVoOXUvzgLXUxOA22h+r/ea+8vQEA4jTVpkK1FNQM0mgzv3ONeneb8upna2PO3WFwr4ySPi5AwGpoBVAVZLfP3M429dZVyq9/uJZMXB8DMLzUDiHjAcQL0tdwE6Tap1C9TqPxE+U3LgzDd5KJ7R6Af1/rm2MDEA+9ANox05XrtG//QPlkKrwCdMcAxP8VPhrgQDqebP13+s3vKK9cHBV+YHXCiBUwyF+/YPvblFc/nmj4SIDu/oG98TmL7/088XAYlGYL3FkN5ZOxiYfDYAVi7jxaD7Q2VPA/V8fDH8k/1vDbPQTseYz22/4GrvgB8OktBhwAAAAASUVORK5CYII=') 2 2, pointer",
    },
    {
        'value': 'imported_olovka',
        'label': 'Olovka',
        'description': 'Olovka kao kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/olovka.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAB90lEQVR4nN3XMWgTURzH8e9fOsQQ0MHJjg5OIq4OxsEO1qVDFDodiFMWFzuHzHYSabdCHATJIoJ1EMWIg95hrUMEwdBbFD1dBIPS5edwr/GuJJqjdxfwD1nuhfv8Xt7l3f8ZxVYFOALUEtd+Ad+BHwBWIH4UOAtcAOaBqrv+GXgIvAC+FYkvAfc0poBXQIP0L5M7ftdhA+DnmBDrwPyhAvDzwBVJy2a2DRyWVMnZmYgv8Wfmb4CPE5bgNTkvQRZ8G7gKHPsv8AqwANyZBQ7x7K85ICgbh/ghWgA2gEHZOO6mHtCbJe47bHcW+NY+dDfxPHil4okQT4DlWeFBVnwuI34JuC7pTLvdHg20Wi3M7C1wG3hMhtfstP1ACl+9uYoMQKzcWNnDbwEPsuDTBkjha+trmAwhms3mgfBpAqTwTqczGvA878D4vwKk8G63675tXG40csH/FiCFP9rcBAMBixcXc8MnBUjhvV5vNFCv13PFx1Xqfx4EgQLfl+/7pWyvNeI2KZCkfr8ff971S8EBTuAaizAMFe7sKAzD0vAa8Rb6QZK+RpGiKCoNh3j2G5I0HA6Te/tW0fgccV930oWgWq1iZgPgJXAfeEaBR6i9AMclnTOz58QnmaeAD3zCHSKLKnMBTgOnHPge+FI0vL8qxB1uKUeoZP0GGmsHjkarRZYAAAAASUVORK5CYII=') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAB90lEQVR4nN3XMWgTURzH8e9fOsQQ0MHJjg5OIq4OxsEO1qVDFDodiFMWFzuHzHYSabdCHATJIoJ1EMWIg95hrUMEwdBbFD1dBIPS5edwr/GuJJqjdxfwD1nuhfv8Xt7l3f8ZxVYFOALUEtd+Ad+BHwBWIH4UOAtcAOaBqrv+GXgIvAC+FYkvAfc0poBXQIP0L5M7ftdhA+DnmBDrwPyhAvDzwBVJy2a2DRyWVMnZmYgv8Wfmb4CPE5bgNTkvQRZ8G7gKHPsv8AqwANyZBQ7x7K85ICgbh/ghWgA2gEHZOO6mHtCbJe47bHcW+NY+dDfxPHil4okQT4DlWeFBVnwuI34JuC7pTLvdHg20Wi3M7C1wG3hMhtfstP1ACl+9uYoMQKzcWNnDbwEPsuDTBkjha+trmAwhms3mgfBpAqTwTqczGvA878D4vwKk8G63675tXG40csH/FiCFP9rcBAMBixcXc8MnBUjhvV5vNFCv13PFx1Xqfx4EgQLfl+/7pWyvNeI2KZCkfr8ff971S8EBTuAaizAMFe7sKAzD0vAa8Rb6QZK+RpGiKCoNh3j2G5I0HA6Te/tW0fgccV930oWgWq1iZgPgJXAfeEaBR6i9AMclnTOz58QnmaeAD3zCHSKLKnMBTgOnHPge+FI0vL8qxB1uKUeoZP0GGmsHjkarRZYAAAAASUVORK5CYII=') 2 2, pointer",
    },
    {
        'value': 'imported_ruza2',
        'label': 'Ruža 2',
        'description': 'Ruža kao kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/ruza2.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAEc0lEQVR4nMXXbWxTVRzH8W9vn7tubQdDMp46AokEYxsSo+/oXojGNzRREqOJq9H4At+UYDCGCA0JPkVjiQmKCdmAKCISt6gJiIldgkTAQGfYVBjbWugcfbi7t2t7e2+ffKHEZrDIw2X+3t17c87/k3PPPeceuIOUPz81Lr520HUnbf4rptk3Um98ssLh9PhtLlcsfuSbsGPNqoDv0y3dyt7vd1qXLPCqo1N+YFAvgKH5YnjT6y5X13KpUlRRivVY7koqsKTbF1+2amWfwWyMGhe0YtjwsGGuzu4mAkD9qzMupfeHD9u8yyTbwg7a1z5Io94IFP8UUSZz/sK0GFYkiVpBof7dhZ26A4RnHpXliaT3+sVrTF/NkhkZZyo+is3TiiYWyFwc9Y4fP8nYtyeoqGpIdwDA9KXRvvxkgtTPI4zH4pSlAma7FYvTjmNxB551flLDI0z9dNYr7jm2QnfAmsNvDYxJyfD5sTjFKREaQKNBowGC2Yxz+RLWvtJD4vwFlJzo1QtgOvfk9t7EqV9DnpWdOBa2YbJZcHS4uXp6GK2kospFZiazWDxOLO1teFavJnlSt48A4ZHju1+sliteRZyZqJYr2NvbaF+5lPy1LIqYp5ieRp6YIn3+Mg1FpX11FwaDIa4bAODZ6vGE2WENGQQDRosZs91KV7efUloin8oiJdJM/vIH4kgCwWiJP3b6kKwrAOCJS72DNa0aU3J5ZiazdAXWkaFIMS0hJ68jJ64zduIcP57pl/QqDrMWoti6zS7BYpqwtjnclhY7yatJzDmNslQAYLjzMme6LmK04x04SkJ3AMDJNS/5gH7AW1UrlOUip4y/I28cY8ak9DUgZG4h+Nn7DOgBuGkvePy3/UNA18CiTb6aVnUPbzgbbH0qFa7L8JDH2zecnMBoxA/3CXAjG9NHhwB2b0QSIOy0WSX3IlfUM0O4ViegR3FomoRzZfvzDOVy9KczakjMZNyd7s6AIMwjACCXJaTkCaauTIYwVSMLPQbePowuy/FtAQ7sQu5YRqTVi1uckqJGs9VbSOtR/i7z5kdc2H2Ir/Xo67ZGYHZKOQL1Cv7IPnr/F8AHEWQpSVAwEnzvKD3zDvgHMSRfI1CWid4L4p7/77ZG8LmWEhNMRC+PEa3XCNU1gnUN6hr9Rz5mz30F3EA4FhNLi9Bo4K7VoKpBpQyNCv7Dexiaq+2cK2Fztu3FZbMRtdqIbX+OA7Ofa06olqDFidsA1GqgaVA2Q6VMCNgyV993NAI7e+mpVAhlU/TXjMT272Bo87v4LBZiNjtuiwUEAapVUFUoFUBMIik5/P1f3Hr3vKtX8PQLrDe7CJmdhByt0NoGLS1gtUG9DmUFJAnkDGh5qBaJHTtIt26AG+nZgctqJWS3E7TaCJhM0GhApfI3olQCtQCVPHy579a1dD3lNCccZYVaJlQuEfC04HcvILzj5Zvnz30DNGdrBF9LB1GTFaoqkV2v/nu2nBdAE2S9zUWf0cKEViTyzjYG5xXQDHE+QLiq4v0LRNTe9ADFZecAAAAASUVORK5CYII=') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAEc0lEQVR4nMXXbWxTVRzH8W9vn7tubQdDMp46AokEYxsSo+/oXojGNzRREqOJq9H4At+UYDCGCA0JPkVjiQmKCdmAKCISt6gJiIldgkTAQGfYVBjbWugcfbi7t2t7e2+ffKHEZrDIw2X+3t17c87/k3PPPeceuIOUPz81Lr520HUnbf4rptk3Um98ssLh9PhtLlcsfuSbsGPNqoDv0y3dyt7vd1qXLPCqo1N+YFAvgKH5YnjT6y5X13KpUlRRivVY7koqsKTbF1+2amWfwWyMGhe0YtjwsGGuzu4mAkD9qzMupfeHD9u8yyTbwg7a1z5Io94IFP8UUSZz/sK0GFYkiVpBof7dhZ26A4RnHpXliaT3+sVrTF/NkhkZZyo+is3TiiYWyFwc9Y4fP8nYtyeoqGpIdwDA9KXRvvxkgtTPI4zH4pSlAma7FYvTjmNxB551flLDI0z9dNYr7jm2QnfAmsNvDYxJyfD5sTjFKREaQKNBowGC2Yxz+RLWvtJD4vwFlJzo1QtgOvfk9t7EqV9DnpWdOBa2YbJZcHS4uXp6GK2kospFZiazWDxOLO1teFavJnlSt48A4ZHju1+sliteRZyZqJYr2NvbaF+5lPy1LIqYp5ieRp6YIn3+Mg1FpX11FwaDIa4bAODZ6vGE2WENGQQDRosZs91KV7efUloin8oiJdJM/vIH4kgCwWiJP3b6kKwrAOCJS72DNa0aU3J5ZiazdAXWkaFIMS0hJ68jJ64zduIcP57pl/QqDrMWoti6zS7BYpqwtjnclhY7yatJzDmNslQAYLjzMme6LmK04x04SkJ3AMDJNS/5gH7AW1UrlOUip4y/I28cY8ak9DUgZG4h+Nn7DOgBuGkvePy3/UNA18CiTb6aVnUPbzgbbH0qFa7L8JDH2zecnMBoxA/3CXAjG9NHhwB2b0QSIOy0WSX3IlfUM0O4ViegR3FomoRzZfvzDOVy9KczakjMZNyd7s6AIMwjACCXJaTkCaauTIYwVSMLPQbePowuy/FtAQ7sQu5YRqTVi1uckqJGs9VbSOtR/i7z5kdc2H2Ir/Xo67ZGYHZKOQL1Cv7IPnr/F8AHEWQpSVAwEnzvKD3zDvgHMSRfI1CWid4L4p7/77ZG8LmWEhNMRC+PEa3XCNU1gnUN6hr9Rz5mz30F3EA4FhNLi9Bo4K7VoKpBpQyNCv7Dexiaq+2cK2Fztu3FZbMRtdqIbX+OA7Ofa06olqDFidsA1GqgaVA2Q6VMCNgyV993NAI7e+mpVAhlU/TXjMT272Bo87v4LBZiNjtuiwUEAapVUFUoFUBMIik5/P1f3Hr3vKtX8PQLrDe7CJmdhByt0NoGLS1gtUG9DmUFJAnkDGh5qBaJHTtIt26AG+nZgctqJWS3E7TaCJhM0GhApfI3olQCtQCVPHy579a1dD3lNCccZYVaJlQuEfC04HcvILzj5Zvnz30DNGdrBF9LB1GTFaoqkV2v/nu2nBdAE2S9zUWf0cKEViTyzjYG5xXQDHE+QLiq4v0LRNTe9ADFZecAAAAASUVORK5CYII=') 2 2, pointer",
    },
    {
        'value': 'imported_sladoled',
        'label': 'Sladoled',
        'description': 'Sladoled kao kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/sladoled.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAE6UlEQVR4nL2X3W8UVRjGn3NmZrttt9giuyXaiiKm0TaRb8INxotiQkks3EgKRGKMV8hfYKIX3njhF4kXgsGQaGqq0UQupCEmpgUaEogfhSAgUii0tNt2v3dmzsf7erGsYNia7rbhTU4ymZPM8zvPc945M2IkfugsgK14uEYARLYmD2+sMLdk5QJA5/PPjgNof1D80uXrD4m3tbW51lohhDATExO8VADl1Zch/iPe3t4u+/r6+nbs2PFWZ2fXWtdz665du3ZzaGjohy+PHfvw4sWL04siGIkf4uy2T8vj7Ej80PnyXEdHR8Pg4OAJYwwba1lpzb4fcC6f51QqzX+Mjk50d3dvWSzA2UriLS0tor+//yutDRMRExEbYzgMQy4UCpzOZDg5M8O//f77VEdHR1ut+hJABBUyX7du3ZZXe3v7AAYRg4jAzOAHkhcQSCRaE/v2739nMQCotOF6enpeA7MgIjw4mAnEDDDAYACM7d3be+sbGupqAXDna7PWlSs7rKUSpSwtu+zEvzDEYGYkWlsTEc9b7gOTVQPMN6GUMtZaMBiSGEIADICIYC3BkoUlAlkCWcvGGKpWHLgXQaUaGxu7oo2BMQbGaJSvrbVgopIbtgRx5erVW0qpdC0AFR1YEY/Lrs6uDUZrEDmQQgBCAACYGUT2vgvWYnh46JdYLKZSqdTSAOzZs+ftjZs2vUxMkCxBzCBmMN/PXQgBKR0wa+zdu+91x3GLn3z80cF8Pl/VG7JiBI7jrgQzbn9zGrcOHMHtXYcxefRnmFCDiHBz4DTOb34P57Z/gPSlcUQiEdGzc+cboVKxah0QlW7WR+qi767ZdXKXfO6lOulAMqBTeczECGGdRP24D0uMvLGYhUK4rc18kR86eObM6SPW2qocqBiBr8KgJStdGyNowZAMcEMdHssG0KGCgoRmW4I1EmbwpjNihwcsqOoDat42TKtiRmkDYxieKwEGKOLACoBCDWvK+wLwoYsE6GrF/xfgrsreCJSBJwQoLLU4McFahpGAdWWpC5hxmacuACguGcAzzuOJ9c5Tvb7SsELCAQBmMDEsMTQRNBEsAMuMAquZOGJNd5HNVAtQsQte8breX+bGnpRPNCO9ysNUq4XyJAJtEGgN4wqMx/MoropAtjRgMz+9ez82n4jCc6oFqOjAn5j+dU1j9spPEydbqTnVvGp5FHGOY339BggrMOIOI9l4F8k84cX6Tdi4+gVOTKnVpmA9ALYagIptKCAEg71EU+SztW1Nb66IRdDc4CEIFbQyaIy6yAUGYzM+bmX1eCYtdzN4Lofw72odqBjBvVNf5QLTL6UAEyFQBk31EaxobkAxNPAVQToSecVfZxGcr0V8XoBy+ZpG0r65YYnhCkBKCYKAUgbGEnwrwlxoj9UivCAAAP5kJvxeOg4a6iNQxpacaIwCUiJZsKeMpZpWvlAATGfD/oKy7GuCMRaeI6AISAcWc745iio3XdUAvqbRZF6N+qFBtM5DxPMwnfGRLNJfuWJ4ajHiCwIAoMbngu+UJWSLGnOFEL4mJAv2OAD/UQBgOhcOzBaMsQzM5UKklChmiuHxxYovGEBbvj6eCs7lQ4vZvMJU3vyojb3zyAAAmMlM8O2dTIhZnzgX2M8B1PQRWnM5Em3tLVG/dVn0AoCa/gEWW3JZ1B2IuPLAUj70Hz2jEyhARM6HAAAAAElFTkSuQmCC') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAE6UlEQVR4nL2X3W8UVRjGn3NmZrttt9giuyXaiiKm0TaRb8INxotiQkks3EgKRGKMV8hfYKIX3njhF4kXgsGQaGqq0UQupCEmpgUaEogfhSAgUii0tNt2v3dmzsf7erGsYNia7rbhTU4ymZPM8zvPc945M2IkfugsgK14uEYARLYmD2+sMLdk5QJA5/PPjgNof1D80uXrD4m3tbW51lohhDATExO8VADl1Zch/iPe3t4u+/r6+nbs2PFWZ2fXWtdz665du3ZzaGjohy+PHfvw4sWL04siGIkf4uy2T8vj7Ej80PnyXEdHR8Pg4OAJYwwba1lpzb4fcC6f51QqzX+Mjk50d3dvWSzA2UriLS0tor+//yutDRMRExEbYzgMQy4UCpzOZDg5M8O//f77VEdHR1ut+hJABBUyX7du3ZZXe3v7AAYRg4jAzOAHkhcQSCRaE/v2739nMQCotOF6enpeA7MgIjw4mAnEDDDAYACM7d3be+sbGupqAXDna7PWlSs7rKUSpSwtu+zEvzDEYGYkWlsTEc9b7gOTVQPMN6GUMtZaMBiSGEIADICIYC3BkoUlAlkCWcvGGKpWHLgXQaUaGxu7oo2BMQbGaJSvrbVgopIbtgRx5erVW0qpdC0AFR1YEY/Lrs6uDUZrEDmQQgBCAACYGUT2vgvWYnh46JdYLKZSqdTSAOzZs+ftjZs2vUxMkCxBzCBmMN/PXQgBKR0wa+zdu+91x3GLn3z80cF8Pl/VG7JiBI7jrgQzbn9zGrcOHMHtXYcxefRnmFCDiHBz4DTOb34P57Z/gPSlcUQiEdGzc+cboVKxah0QlW7WR+qi767ZdXKXfO6lOulAMqBTeczECGGdRP24D0uMvLGYhUK4rc18kR86eObM6SPW2qocqBiBr8KgJStdGyNowZAMcEMdHssG0KGCgoRmW4I1EmbwpjNihwcsqOoDat42TKtiRmkDYxieKwEGKOLACoBCDWvK+wLwoYsE6GrF/xfgrsreCJSBJwQoLLU4McFahpGAdWWpC5hxmacuACguGcAzzuOJ9c5Tvb7SsELCAQBmMDEsMTQRNBEsAMuMAquZOGJNd5HNVAtQsQte8breX+bGnpRPNCO9ysNUq4XyJAJtEGgN4wqMx/MoropAtjRgMz+9ez82n4jCc6oFqOjAn5j+dU1j9spPEydbqTnVvGp5FHGOY339BggrMOIOI9l4F8k84cX6Tdi4+gVOTKnVpmA9ALYagIptKCAEg71EU+SztW1Nb66IRdDc4CEIFbQyaIy6yAUGYzM+bmX1eCYtdzN4Lofw72odqBjBvVNf5QLTL6UAEyFQBk31EaxobkAxNPAVQToSecVfZxGcr0V8XoBy+ZpG0r65YYnhCkBKCYKAUgbGEnwrwlxoj9UivCAAAP5kJvxeOg4a6iNQxpacaIwCUiJZsKeMpZpWvlAATGfD/oKy7GuCMRaeI6AISAcWc745iio3XdUAvqbRZF6N+qFBtM5DxPMwnfGRLNJfuWJ4ajHiCwIAoMbngu+UJWSLGnOFEL4mJAv2OAD/UQBgOhcOzBaMsQzM5UKklChmiuHxxYovGEBbvj6eCs7lQ4vZvMJU3vyojb3zyAAAmMlM8O2dTIhZnzgX2M8B1PQRWnM5Em3tLVG/dVn0AoCa/gEWW3JZ1B2IuPLAUj70Hz2jEyhARM6HAAAAAElFTkSuQmCC') 2 2, pointer",
    },
    {
        'value': 'imported_srce2',
        'label': 'Srce 2',
        'description': 'Rozo srce kao kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/srce2.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAELUlEQVR4nO2Wy2/cVBSHv3PtNGnStEnDBAqCIhBUQIEFQmxYsgM14iEkVogl6d/TCJb8A0jpEiSQUKtKiEVVlafoIyltM690Mm+P7fvrwm4yncx00kTseiRb9r3n3vP5+Dyulb767gOi5GWwQySpo5cEgAelQKwwaCF18WogGhhb8qobqiFiIAXSp8+fTdmHhOb9mzwz/3Eq9xSOgDRFSSqSVERxlziNSNKmpWmNVFXzqjloIKsCGxgVRLl0ZmUTaIM6i48BE5rZzNSnb53yzhZ9MyJtRqjVxbcjqd0zdWLUjvHNCFo9Tyfesii562J/De+vm7gJFM1oS2wCxfLSSgWoF1aXk3EADq/QJoLwkVoGNhFgU6Gz6Yl5zRx6zU+FH/kw+FLOPgfekThqxgLwKvA68GJ5aeXIeID9isMIbE7O3vPGF8D7wOF89gjwPPBSeWll7v8B2BZzmJ2Q8YngNBDkEwEwD5wsL63MjgPQQSmABeBDYGZgfBZ4try0MjkcwIjV7fUASSiH0fZdEqD8QULKifPxfF02eRqYV67dd81LmiudOWe7AOz4dJtuEgNmhuXUtn03M8DyBzPM8k/Lx/N1ZmZGAMxZrp1fD2Send+zA6BEHd/qdfbh9mHigVF7Hc4/7mEA0rSuRqfFweMA4A5QHTEXjgBQTdVWHbMDAigCfgQaoxSGDTqcVXyxUTdn8QGsd4AfgAtAb4RONAwiJE7LqnfbNLp1oDDWlACvPwkcJJqW+aJDFw2uGGw9wo0NshgZAAiDe2pF5fR2bUMnji3w4D/tpGH+mm9twppR0yX+WzM8XjGQAGmemnnmPoQcAZVhTcqp00sUJWu6Uys5R8xe0jBw0y5j0WDKAQyMJWa2YWbtYW5xdOMEr3VfrFfViDax8dlgUn+kK3ft4DoPtIBbQKmwurzL/ZDFQEwYrGmjUdWNyjU7uXBMO01lt3jfscRfGTBUzI1NkXmwC9SBCrBVWF0eeT4IC99/nZY/+6aoKCmlv9/9O5iZPMb0xClgYpe2iKyTXDCv632jjizA/iGrdA6IgWgv54HsHJD4OsaaKq3Z9Le1X93bzyWaDF9R1lYz0/L3rBVddO3eJVCnr6YYmcdUWF2ujzM4HEA0gXXQGyo1qukv//7M4uxld3SqoNRPqN6tWq1zi3ZcMakjMVjTQobU+T0DFFaX49KZc+tAGXGcTtxlbfMWcANILE8zIBmRaj0ytz+2bB9IzOy2mf1hZnGeTf3d7KHU6pvDzFIza5hZdCCAwupyG7gMrLP3xiRgiyzN9tVLBo9k/wGXyDraXjbsAteBzf0Y3wWQf8VfwE/AvTFr28BV4Oaj8nyc7OrPAOWllVDSCTN7F3iBrCakZMHYlLRuZleBamF1+SBddDhAH8gUMElWDybJXN6UFC2eP7uvoHsiT2RQ7gOhQzXK+5OubAAAAABJRU5ErkJggg==') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAELUlEQVR4nO2Wy2/cVBSHv3PtNGnStEnDBAqCIhBUQIEFQmxYsgM14iEkVogl6d/TCJb8A0jpEiSQUKtKiEVVlafoIyltM690Mm+P7fvrwm4yncx00kTseiRb9r3n3vP5+Dyulb767gOi5GWwQySpo5cEgAelQKwwaCF18WogGhhb8qobqiFiIAXSp8+fTdmHhOb9mzwz/3Eq9xSOgDRFSSqSVERxlziNSNKmpWmNVFXzqjloIKsCGxgVRLl0ZmUTaIM6i48BE5rZzNSnb53yzhZ9MyJtRqjVxbcjqd0zdWLUjvHNCFo9Tyfesii562J/De+vm7gJFM1oS2wCxfLSSgWoF1aXk3EADq/QJoLwkVoGNhFgU6Gz6Yl5zRx6zU+FH/kw+FLOPgfekThqxgLwKvA68GJ5aeXIeID9isMIbE7O3vPGF8D7wOF89gjwPPBSeWll7v8B2BZzmJ2Q8YngNBDkEwEwD5wsL63MjgPQQSmABeBDYGZgfBZ4try0MjkcwIjV7fUASSiH0fZdEqD8QULKifPxfF02eRqYV67dd81LmiudOWe7AOz4dJtuEgNmhuXUtn03M8DyBzPM8k/Lx/N1ZmZGAMxZrp1fD2Send+zA6BEHd/qdfbh9mHigVF7Hc4/7mEA0rSuRqfFweMA4A5QHTEXjgBQTdVWHbMDAigCfgQaoxSGDTqcVXyxUTdn8QGsd4AfgAtAb4RONAwiJE7LqnfbNLp1oDDWlACvPwkcJJqW+aJDFw2uGGw9wo0NshgZAAiDe2pF5fR2bUMnji3w4D/tpGH+mm9twppR0yX+WzM8XjGQAGmemnnmPoQcAZVhTcqp00sUJWu6Uys5R8xe0jBw0y5j0WDKAQyMJWa2YWbtYW5xdOMEr3VfrFfViDax8dlgUn+kK3ft4DoPtIBbQKmwurzL/ZDFQEwYrGmjUdWNyjU7uXBMO01lt3jfscRfGTBUzI1NkXmwC9SBCrBVWF0eeT4IC99/nZY/+6aoKCmlv9/9O5iZPMb0xClgYpe2iKyTXDCv632jjizA/iGrdA6IgWgv54HsHJD4OsaaKq3Z9Le1X93bzyWaDF9R1lYz0/L3rBVddO3eJVCnr6YYmcdUWF2ujzM4HEA0gXXQGyo1qukv//7M4uxld3SqoNRPqN6tWq1zi3ZcMakjMVjTQobU+T0DFFaX49KZc+tAGXGcTtxlbfMWcANILE8zIBmRaj0ytz+2bB9IzOy2mf1hZnGeTf3d7KHU6pvDzFIza5hZdCCAwupyG7gMrLP3xiRgiyzN9tVLBo9k/wGXyDraXjbsAteBzf0Y3wWQf8VfwE/AvTFr28BV4Oaj8nyc7OrPAOWllVDSCTN7F3iBrCakZMHYlLRuZleBamF1+SBddDhAH8gUMElWDybJXN6UFC2eP7uvoHsiT2RQ7gOhQzXK+5OubAAAAABJRU5ErkJggg==') 2 2, pointer",
    },
    {
        'value': 'imported_vatra',
        'label': 'Vatra',
        'description': 'Vatra kao kursor.',
        'preview_html': _cursor_preview_markup('<img src="/static/blog/cursors/custom/previews/vatra.png" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAADWUlEQVR4nO3XS28bVRjG8f+5zMVz8/gex0njxqbQSt0QVAkWbBBbhISQukGR4KtQIcHn4DtUVVkgdVM2FQKJS5qWElRSIKmd2E4cj89hYYREk0DtJIqQ+i5Hc+b9nefMHJ0RgOUcS55n86kAq/X6+QJCKbler/N+43Qh/wn4+MISABWlqWmNMvDeKSKeK4FP2y1cIXi7ledaKSQ4xVfnuZ7kBw5R5LHQytOqRlzUDh82GmcPuLHURAh49WJEreQTlOClq3lWWikLSrF6CohjAZ80mzhK8tZrNeK8JslJnnZHlBqw3Ap5/ZUiy57DRydEHAvQSnG1nVAoa0qXNG9cT0giSZAailVJvRqw0kxZyHl8cAKEPuriZ+0WUeRQrIbkEks+FPhFydzLDrmSg2DEeCSwmU9mDL2H2cyAIxPI+Zr2fEQaWoK8QAcSxpak6aEaPuGiR/GKJJmT1Gs5ajmX1QuzpXBkAo5WxKlHVLT4JfDLAgIJFQ/qeRAdQgzVy2BGcO1SypNvRzMBDiVw40obL9AkMeRrirDqQaLB1xB4kM9B7IGWRA2HZElRKngUtZ5plzwEkFJyeTmmWJa4NQ2xC5UI6jHEKfghRB4owIPCkiJIYKUd48+wQR1aggNr8BT4qcBJFBQCSFIouhDUIZNQ3J0sya5B+hCWIf1FE0/d/ogE9jODBZQPRBJKEcwVIGjDuAlmDoIE5sO/h4tAEkYuOaVODhiMxggAIcGXUAlBz0FWBetPhpgAFgvgaUwGQSRxA3C1ODlgPzPc/a7DYDACKyEAxgmYeHJ2suKvJMrgeYwzQIH0AecUEri9s0u3N2KvaxkPMhDDSRpWY6zD0JoJzITgOWAUw55hY9vl8Wj6T/EQYL3T4dFwSGfTsLdxAP19EHtYDNZqsArkFsg+/Qf7DLcyeluGh7/tcGd79+QAgPXRAbe+7rBx74D+l1042MDqP7Cij1LboLfhp216Pwzo/Jpx98cxN+//znqnMzXgyJ1wbWePSuDi3usxv+ny5uYatXf2kIUSsMXjL4as3driyTc9HvQH3Pn5Kd93+1M3BxAccyxvpSkA77Zr1DyHwmKZqJJjMBjyaGOHz7+6/4/7Z5n9vwKehTxbszacGnDW9f/5MXkBeAE4q/oTxK3vRXtaptIAAAAASUVORK5CYII=') 2 2, auto",
        'pointer_cursor_css': "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAADWUlEQVR4nO3XS28bVRjG8f+5zMVz8/gex0njxqbQSt0QVAkWbBBbhISQukGR4KtQIcHn4DtUVVkgdVM2FQKJS5qWElRSIKmd2E4cj89hYYREk0DtJIqQ+i5Hc+b9nefMHJ0RgOUcS55n86kAq/X6+QJCKbler/N+43Qh/wn4+MISABWlqWmNMvDeKSKeK4FP2y1cIXi7ledaKSQ4xVfnuZ7kBw5R5LHQytOqRlzUDh82GmcPuLHURAh49WJEreQTlOClq3lWWikLSrF6CohjAZ80mzhK8tZrNeK8JslJnnZHlBqw3Ap5/ZUiy57DRydEHAvQSnG1nVAoa0qXNG9cT0giSZAailVJvRqw0kxZyHl8cAKEPuriZ+0WUeRQrIbkEks+FPhFydzLDrmSg2DEeCSwmU9mDL2H2cyAIxPI+Zr2fEQaWoK8QAcSxpak6aEaPuGiR/GKJJmT1Gs5ajmX1QuzpXBkAo5WxKlHVLT4JfDLAgIJFQ/qeRAdQgzVy2BGcO1SypNvRzMBDiVw40obL9AkMeRrirDqQaLB1xB4kM9B7IGWRA2HZElRKngUtZ5plzwEkFJyeTmmWJa4NQ2xC5UI6jHEKfghRB4owIPCkiJIYKUd48+wQR1aggNr8BT4qcBJFBQCSFIouhDUIZNQ3J0sya5B+hCWIf1FE0/d/ogE9jODBZQPRBJKEcwVIGjDuAlmDoIE5sO/h4tAEkYuOaVODhiMxggAIcGXUAlBz0FWBetPhpgAFgvgaUwGQSRxA3C1ODlgPzPc/a7DYDACKyEAxgmYeHJ2suKvJMrgeYwzQIH0AecUEri9s0u3N2KvaxkPMhDDSRpWY6zD0JoJzITgOWAUw55hY9vl8Wj6T/EQYL3T4dFwSGfTsLdxAP19EHtYDNZqsArkFsg+/Qf7DLcyeluGh7/tcGd79+QAgPXRAbe+7rBx74D+l1042MDqP7Cij1LboLfhp216Pwzo/Jpx98cxN+//znqnMzXgyJ1wbWePSuDi3usxv+ny5uYatXf2kIUSsMXjL4as3driyTc9HvQH3Pn5Kd93+1M3BxAccyxvpSkA77Zr1DyHwmKZqJJjMBjyaGOHz7+6/4/7Z5n9vwKehTxbszacGnDW9f/5MXkBeAE4q/oTxK3vRXtaptIAAAAASUVORK5CYII=') 2 2, pointer",
    },
)



EXTERNAL_CURSOR_HOTSPOT_OVERRIDES = {
    'lollipop': (16, 16),
    'pointy_hand': (8, 4),
    'leaf': (9, 26),
    'bear_paw_print': (16, 16),
    'large_rainbow_pointer': (6, 4),
    'free_lines_arrow': (6, 4),
    'metal_set_handwriting': (9, 24),
    'harry_potter_magical_wand': (5, 5),
    'harry_potter_nimbus_2000_broom': (6, 10),
    'chrome_handwriting': (10, 26),
    'sexy_pink_heart': (16, 16),
    'vindictus_hero_drag_burn': (16, 16),
}


def _normalize_external_cursor_css(choice, css_value):
    if not css_value:
        return css_value

    css_text = str(css_value)
    if 'cdn.cursors-4u.net/previews/' not in css_text:
        return css_value

    match = re.search(r"url\('([^']+)'\)\s+(\d+)\s+(\d+),\s*(auto|pointer)", css_text)
    if not match:
        return css_value

    url, hot_x, hot_y, fallback = match.groups()
    hot_x = int(hot_x)
    hot_y = int(hot_y)

    override = EXTERNAL_CURSOR_HOTSPOT_OVERRIDES.get(str(choice.get('value', '') or '').strip())
    if override is not None:
        safe_x, safe_y = override
    else:
        safe_x = min(hot_x, 30)
        safe_y = min(hot_y, 30)

    return f"url('{url}') {safe_x} {safe_y}, {fallback}"


def _sanitize_cursor_css_png(css_value):
    if Image is None or not css_value:
        return css_value

    match = re.search(r"data:image/png;base64,([^']+)", str(css_value))
    if not match:
        return css_value

    encoded = match.group(1)

    try:
        image = Image.open(io.BytesIO(base64.b64decode(encoded))).convert("RGBA")
    except Exception:
        return css_value

    width, height = image.size
    pixels = image.load()

    has_real_transparency = False
    for y in range(height):
        for x in range(width):
            if pixels[x, y][3] < 250:
                has_real_transparency = True
                break
        if has_real_transparency:
            break

    if has_real_transparency:
        return css_value

    def is_background(px):
        r, g, b, a = px
        return a >= 245 and r <= 24 and g <= 24 and b <= 24

    queue = deque()
    visited = set()

    def push(x, y):
        if (x, y) in visited:
            return
        if not is_background(pixels[x, y]):
            return
        visited.add((x, y))
        queue.append((x, y))

    for x in range(width):
        push(x, 0)
        push(x, height - 1)

    for y in range(height):
        push(0, y)
        push(width - 1, y)

    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < width and 0 <= ny < height:
                push(nx, ny)

    if len(visited) < max(20, (width * height) // 10):
        return css_value

    for x, y in visited:
        r, g, b, _ = pixels[x, y]
        pixels[x, y] = (r, g, b, 0)

    output = io.BytesIO()
    try:
        image.save(output, format="PNG")
    except Exception:
        return css_value

    new_encoded = base64.b64encode(output.getvalue()).decode("ascii")
    return str(css_value).replace(encoded, new_encoded, 1)


def _normalize_imported_cursor_choice(choice):
    choice = choice.copy()
    value = str(choice.get('value', '') or '')

    if value.startswith('imported_'):
        choice['cursor_css'] = _sanitize_cursor_css_png(choice.get('cursor_css', ''))
        choice['pointer_cursor_css'] = _sanitize_cursor_css_png(choice.get('pointer_cursor_css', ''))

    choice['cursor_css'] = _normalize_external_cursor_css(choice, choice.get('cursor_css', ''))
    choice['pointer_cursor_css'] = _normalize_external_cursor_css(choice, choice.get('pointer_cursor_css', ''))
    return choice


BLOG_CURSOR_CHOICES = [_normalize_imported_cursor_choice(item) for item in (BLOG_CURSOR_CHOICES + IMPORTED_CURSOR_CHOICES)]

BLOG_CURSOR_VALUES = {item['value'] for item in BLOG_CURSOR_CHOICES}

BLOG_CURSOR_EFFECT_CHOICES = (
    {
        'value': 'none',
        'label': 'Bez efekta',
        'description': 'Samo odabrani kursor, bez dodatne animacije.',
        'preview_html': _cursor_preview_markup('<span class="ambience-effect-demo ambience-effect-demo--none" aria-hidden="true"></span>'),
    },
    {
        'value': 'glow',
        'label': 'Sjaj',
        'description': 'Meki svjetleći krug prati miš dok se pomiče.',
        'preview_html': _cursor_preview_markup('<span class="ambience-effect-demo ambience-effect-demo--glow" aria-hidden="true"></span>'),
    },
    {
        'value': 'sparkles',
        'label': 'Iskrice',
        'description': 'Sitne iskrice kratko ostaju iza kursora.',
        'preview_html': _cursor_preview_markup('<span class="ambience-effect-demo ambience-effect-demo--sparkles" aria-hidden="true"></span>'),
    },
    {
        'value': 'dots',
        'label': 'Točkice',
        'description': 'Mali trag točkica prati pomicanje miša.',
        'preview_html': _cursor_preview_markup('<span class="ambience-effect-demo ambience-effect-demo--dots" aria-hidden="true"></span>'),
    },
    {
        'value': 'mist',
        'label': 'Maglica',
        'description': 'Lagana maglica se raspline iza kursora.',
        'preview_html': _cursor_preview_markup('<span class="ambience-effect-demo ambience-effect-demo--mist" aria-hidden="true"></span>'),
    },
    {
        'value': 'rings',
        'label': 'Prstenovi',
        'description': 'Prozirni krugovi se šire iza kursora.',
        'preview_html': _cursor_preview_markup('<span class="ambience-effect-demo ambience-effect-demo--rings" aria-hidden="true"></span>'),
    },
    {
        'value': 'hearts',
        'label': 'Srca',
        'description': 'Mala srca lebde iza kursora.',
        'preview_html': _cursor_preview_markup('<span class="ambience-effect-demo ambience-effect-demo--hearts" aria-hidden="true"></span>'),
    },
    {
        'value': 'embers',
        'label': 'Žeravica',
        'description': 'Topli narančasti žar i sitne iskre.',
        'preview_html': _cursor_preview_markup('<span class="ambience-effect-demo ambience-effect-demo--embers" aria-hidden="true"></span>'),
    },
    {
        'value': 'neon',
        'label': 'Neon',
        'description': 'Neonski trag u plavo-roza tonovima.',
        'preview_html': _cursor_preview_markup('<span class="ambience-effect-demo ambience-effect-demo--neon" aria-hidden="true"></span>'),
    },
    {
        'value': 'stardust',
        'label': 'Zvjezdana prašina',
        'description': 'Sitne sjajne zvjezdice ostaju iza kursora.',
        'preview_html': _cursor_preview_markup('<span class="ambience-effect-demo ambience-effect-demo--stardust" aria-hidden="true"></span>'),
    },
    {
        'value': 'electric',
        'label': 'Elektrika',
        'description': 'Kratki plavi električni bljeskovi prate miš.',
        'preview_html': _cursor_preview_markup('<span class="ambience-effect-demo ambience-effect-demo--electric" aria-hidden="true"></span>'),
    },
    {
        'value': 'crystals',
        'label': 'Kristali',
        'description': 'Sitni kristalići se rasprše dok se miš pomiče.',
        'preview_html': _cursor_preview_markup('<span class="ambience-effect-demo ambience-effect-demo--crystals" aria-hidden="true"></span>'),
    },
    {
        'value': 'comet_trail',
        'label': 'Kometni trag',
        'description': 'Mali svijetli trag kao mini kometi iza kursora.',
        'preview_html': _cursor_preview_markup('<span class="ambience-effect-demo ambience-effect-demo--comet-trail" aria-hidden="true"></span>'),
    },
    {
        'value': 'rainbow_orbit',
        'label': 'Dugin rep zmaja',
        'description': 'Fluidniji rep u duginim bojama. I kad miš stane, zadržava oblik i lagano vijori umjesto da se skupi u točku.',
        'preview_html': _cursor_preview_markup('<span class="ambience-effect-demo ambience-effect-demo--rainbow-orbit" aria-hidden="true"></span>'),
    },
    {
        'value': 'silk_tail',
        'label': 'Svileni rep',
        'description': 'Mekani valoviti rep u ružičasto-ljubičastim tonovima. Nježniji i mirniji od duginog.',
        'preview_html': _cursor_preview_markup('<span class="ambience-effect-demo ambience-effect-demo--silk-tail" aria-hidden="true"></span>'),
    },
    {
        'value': 'ocean_tail',
        'label': 'Ledeni rep',
        'description': 'Hladniji rep u plavo-srebrnim tonovima, kao trag leda ili mora.',
        'preview_html': _cursor_preview_markup('<span class="ambience-effect-demo ambience-effect-demo--ocean-tail" aria-hidden="true"></span>'),
    },
    {
        'value': 'ember_tail',
        'label': 'Vatreni rep',
        'description': 'Topli valoviti rep u crveno-narančastim tonovima, kao žeravica i plamen.',
        'preview_html': _cursor_preview_markup('<span class="ambience-effect-demo ambience-effect-demo--ember-tail" aria-hidden="true"></span>'),
    },
    {
        'value': 'moon_tail',
        'label': 'Mjesečev rep',
        'description': 'Mekši srebrno-ljubičasti rep, smireniji i elegantniji dok se kreće i dok miš miruje.',
        'preview_html': _cursor_preview_markup('<span class="ambience-effect-demo ambience-effect-demo--moon-tail" aria-hidden="true"></span>'),
    },
    {
        'value': 'forest_tail',
        'label': 'Šumski rep',
        'description': 'Zeleno-zlatni rep, mirniji i prirodniji od duginog, s blagim valovima.',
        'preview_html': _cursor_preview_markup('<span class="ambience-effect-demo ambience-effect-demo--forest-tail" aria-hidden="true"></span>'),
    },
    {
        'value': 'love_shot',
        'label': 'Love shot',
        'description': 'Na klik ispaljuje mali ljubavni projektil i natpis JUST LOVE koji kratko ostane.',
        'preview_html': _cursor_preview_markup('<span class="ambience-effect-demo ambience-effect-demo--love-shot" aria-hidden="true"></span>'),
    },
    {
        'value': 'confetti_burst',
        'label': 'Konfeti',
        'description': 'Na klik se rasprši šarena eksplozija konfeta.',
        'preview_html': _cursor_preview_markup('<span class="ambience-effect-demo ambience-effect-demo--confetti-burst" aria-hidden="true"></span>'),
    },
    {
        'value': 'bubble_pop',
        'label': 'Mjehurići na klik',
        'description': 'Na klik izlete prozirni mjehurići i plutaju par trenutaka.',
        'preview_html': _cursor_preview_markup('<span class="ambience-effect-demo ambience-effect-demo--bubble-pop" aria-hidden="true"></span>'),
    },
)

BLOG_CURSOR_EFFECT_VALUES = {item['value'] for item in BLOG_CURSOR_EFFECT_CHOICES}

DEFAULT_CURSOR_STYLE = 'default'


def _external_cursor_preview(symbol):
    return _cursor_preview_markup(f'<span style="display:inline-flex;align-items:center;justify-content:center;width:100%;height:100%;font-size:2rem;line-height:1;">{symbol}</span>')


BLOG_CURSOR_CHOICES = (
    {
        'value': 'falling_rose_petals',
        'label': 'Falling Rose Petals',
        'description': 'Animirane latice ruže.',
        'preview_html': _external_cursor_preview('🌹'),
        'cursor_css': 'inherit',
        'pointer_cursor_css': 'inherit',
        'cursor_stylesheet_url': 'https://cdn.cursors-4u.net/cursors/animated/falling-rose-petals-5d0e9737-32.css',
    },
    {
        'value': 'lollipop',
        'label': 'Lollipop',
        'description': 'Slatki kursor lizalica.',
        'preview_html': _cursor_preview_markup('<img src="https://cdn.cursors-4u.net/previews/lollipop-511c4ad3-32.webp" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('https://cdn.cursors-4u.net/previews/lollipop-511c4ad3-32.webp') 33 33, auto",
        'pointer_cursor_css': "url('https://cdn.cursors-4u.net/previews/lollipop-511c4ad3-32.webp') 33 33, pointer",
    },
    {
        'value': 'handwriting_smiley_star',
        'label': 'Handwriting Smiley Star',
        'description': 'Animirana zvjezdica s osmijehom.',
        'preview_html': _external_cursor_preview('⭐'),
        'cursor_css': 'inherit',
        'pointer_cursor_css': 'inherit',
        'cursor_stylesheet_url': 'https://cdn.cursors-4u.net/cursors/animated/handwriting-smiley-star-9774b69d-32.css',
    },
    {
        'value': 'pointy_hand',
        'label': 'Pointy Hand',
        'description': 'Šiljasta ruka.',
        'preview_html': _cursor_preview_markup('<img src="https://cdn.cursors-4u.net/previews/pointy-hand-17ba50e9-32.webp" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('https://cdn.cursors-4u.net/previews/pointy-hand-17ba50e9-32.webp') 37 34, auto",
        'pointer_cursor_css': "url('https://cdn.cursors-4u.net/previews/pointy-hand-17ba50e9-32.webp') 37 34, pointer",
    },
    {
        'value': 'leaf',
        'label': 'Leaf',
        'description': 'Zeleni list.',
        'preview_html': _cursor_preview_markup('<img src="https://cdn.cursors-4u.net/previews/leaf-dc1a29b3-32.webp" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('https://cdn.cursors-4u.net/previews/leaf-dc1a29b3-32.webp') 36 56, auto",
        'pointer_cursor_css': "url('https://cdn.cursors-4u.net/previews/leaf-dc1a29b3-32.webp') 36 56, pointer",
    },
    {
        'value': 'white_paper_airplane',
        'label': 'White Paper Airplane',
        'description': 'Animirani papirnati avion.',
        'preview_html': _external_cursor_preview('✈️'),
        'cursor_css': 'inherit',
        'pointer_cursor_css': 'inherit',
        'cursor_stylesheet_url': 'https://cdn.cursors-4u.net/cursors/animated/paper-airplane-19477b19-32.css',
    },
    {
        'value': 'flaming_soccer_ball',
        'label': 'Flaming Soccer Ball',
        'description': 'Animirana vatrena lopta.',
        'preview_html': _external_cursor_preview('⚽'),
        'cursor_css': 'inherit',
        'pointer_cursor_css': 'inherit',
        'cursor_stylesheet_url': 'https://cdn.cursors-4u.net/cursors/animated/spo17-11-790f151d-32.css',
    },
    {
        'value': 'bear_paw_print',
        'label': 'Bear Paw Print',
        'description': 'Otisak medvjeđe šape.',
        'preview_html': _cursor_preview_markup('<img src="https://cdn.cursors-4u.net/previews/bear-paw-print-f3993f58-32.webp" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('https://cdn.cursors-4u.net/previews/bear-paw-print-f3993f58-32.webp') 32 32, auto",
        'pointer_cursor_css': "url('https://cdn.cursors-4u.net/previews/bear-paw-print-f3993f58-32.webp') 32 32, pointer",
    },
    {
        'value': 'firefly_busy_wait',
        'label': 'Firefly Busy/Wait',
        'description': 'Animirana krijesnica.',
        'preview_html': _external_cursor_preview('✨'),
        'cursor_css': 'inherit',
        'pointer_cursor_css': 'inherit',
        'cursor_stylesheet_url': 'https://cdn.cursors-4u.net/cursors/animated/firefly-busy-wait-c96f64ab-41.css',
    },
    {
        'value': 'large_rainbow_pointer',
        'label': 'Large Rainbow Pointer',
        'description': 'Velika dugina strelica.',
        'preview_html': _cursor_preview_markup('<img src="https://cdn.cursors-4u.net/previews/large-rainbow-pointer-4bad288d-32.webp" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('https://cdn.cursors-4u.net/previews/large-rainbow-pointer-4bad288d-32.webp') 32 32, auto",
        'pointer_cursor_css': "url('https://cdn.cursors-4u.net/previews/large-rainbow-pointer-4bad288d-32.webp') 32 32, pointer",
    },
    {
        'value': 'free_lines_arrow',
        'label': 'Free Lines Arrow',
        'description': 'Tanka crtasta strelica.',
        'preview_html': _cursor_preview_markup('<img src="https://cdn.cursors-4u.net/previews/free-lines-arrow-9f462bf9-32.webp" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('https://cdn.cursors-4u.net/previews/free-lines-arrow-9f462bf9-32.webp') 32 32, auto",
        'pointer_cursor_css': "url('https://cdn.cursors-4u.net/previews/free-lines-arrow-9f462bf9-32.webp') 32 32, pointer",
    },
    {
        'value': 'metal_set_handwriting',
        'label': 'Metal Set Handwriting',
        'description': 'Metalni handwriting stil.',
        'preview_html': _cursor_preview_markup('<img src="https://cdn.cursors-4u.net/previews/metal-set-handwriting-c02c7b50-32.webp" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('https://cdn.cursors-4u.net/previews/metal-set-handwriting-c02c7b50-32.webp') 35 34, auto",
        'pointer_cursor_css': "url('https://cdn.cursors-4u.net/previews/metal-set-handwriting-c02c7b50-32.webp') 35 34, pointer",
    },
    {
        'value': 'harry_potter_magical_wand',
        'label': 'Harry Potter Magical Wand',
        'description': 'Čarobni štapić.',
        'preview_html': _cursor_preview_markup('<img src="https://cdn.cursors-4u.net/previews/harry-potter-magical-wand-ef2c54d6-32.webp" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('https://cdn.cursors-4u.net/previews/harry-potter-magical-wand-ef2c54d6-32.webp') 32 32, auto",
        'pointer_cursor_css': "url('https://cdn.cursors-4u.net/previews/harry-potter-magical-wand-ef2c54d6-32.webp') 32 32, pointer",
    },
    {
        'value': 'harry_potter_nimbus_2000_broom',
        'label': 'Harry Potter Nimbus 2000 Broom',
        'description': 'Nimbus 2000 metla.',
        'preview_html': _cursor_preview_markup('<img src="https://cdn.cursors-4u.net/previews/harry-potter-nimbus-2000-broom-e65a57c9-32.webp" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('https://cdn.cursors-4u.net/previews/harry-potter-nimbus-2000-broom-e65a57c9-32.webp') 32 32, auto",
        'pointer_cursor_css': "url('https://cdn.cursors-4u.net/previews/harry-potter-nimbus-2000-broom-e65a57c9-32.webp') 32 32, pointer",
    },
    {
        'value': 'chrome_handwriting',
        'label': 'Chrome Handwriting',
        'description': 'Kromirani handwriting stil.',
        'preview_html': _cursor_preview_markup('<img src="https://cdn.cursors-4u.net/previews/chrome-handwriting-54cdd65f-32.webp" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('https://cdn.cursors-4u.net/previews/chrome-handwriting-54cdd65f-32.webp') 34 61, auto",
        'pointer_cursor_css': "url('https://cdn.cursors-4u.net/previews/chrome-handwriting-54cdd65f-32.webp') 34 61, pointer",
    },
    {
        'value': 'sexy_pink_heart',
        'label': 'Sexy Pink Heart',
        'description': 'Ružičasto srce.',
        'preview_html': _cursor_preview_markup('<img src="https://cdn.cursors-4u.net/previews/sexy-pink-heart-25412ebd-32.webp" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('https://cdn.cursors-4u.net/previews/sexy-pink-heart-25412ebd-32.webp') 32 32, auto",
        'pointer_cursor_css': "url('https://cdn.cursors-4u.net/previews/sexy-pink-heart-25412ebd-32.webp') 32 32, pointer",
    },
    {
        'value': 'vindictus_hero_drag_burn',
        'label': 'Vindictus Hero Drag Burn',
        'description': 'Vatreni drag burn stil.',
        'preview_html': _cursor_preview_markup('<img src="https://cdn.cursors-4u.net/previews/vindictus-hero-drag-burn-0dc88436-32.webp" alt="" class="ambience-imported-cursor-preview">'),
        'cursor_css': "url('https://cdn.cursors-4u.net/previews/vindictus-hero-drag-burn-0dc88436-32.webp') 32 32, auto",
        'pointer_cursor_css': "url('https://cdn.cursors-4u.net/previews/vindictus-hero-drag-burn-0dc88436-32.webp') 32 32, pointer",
    },
)

BLOG_CURSOR_VALUES = {item['value'] for item in BLOG_CURSOR_CHOICES}


def get_blog_cursor_choices():
    return [item.copy() for item in BLOG_CURSOR_CHOICES]


def get_blog_cursor_effect_choices():
    return [item.copy() for item in BLOG_CURSOR_EFFECT_CHOICES]


def get_cursor_choice(cursor_value):
    for item in BLOG_CURSOR_CHOICES:
        if item.get('value') == cursor_value:
            return item.copy()
    return {'value': DEFAULT_CURSOR_STYLE, 'label': 'Klasični'}



def get_design_font_choices():
    return [
        {
            'value': value,
            'label': label,
            'stack': DESIGN_FONT_STACKS.get(value, DESIGN_FONT_STACKS['georgia']),
        }
        for value, label in DEFAULT_DESIGN_FONT_CHOICES
    ]


def get_design_pattern_choices():
    return [
        {'value': value, 'label': label, 'asset': DESIGN_PATTERN_ASSETS.get(value, '')}
        for value, label in DESIGN_PATTERN_CHOICES
    ]


def get_design_background_image_choices():
    return [
        {'value': value, 'label': label, 'asset': DESIGN_BACKGROUND_IMAGE_ASSETS.get(value, '')}
        for value, label in DESIGN_BACKGROUND_IMAGE_CHOICES
    ]


def get_soho_cover_image_choices():
    return [
        {'value': value, 'label': label, 'asset': SOHO_COVER_IMAGE_ASSETS.get(value, '')}
        for value, label in SOHO_COVER_IMAGE_CHOICES
    ]


def get_design_gradient_direction_choices():
    return [
        {'value': 'to bottom', 'label': 'Odozgo prema dolje'},
        {'value': 'to right', 'label': 'S lijeva na desno'},
        {'value': '135deg', 'label': 'Dijagonalno'},
    ]


def is_right_layout_design_template(template_name):
    return template_name in RIGHT_LAYOUT_DESIGN_TEMPLATES


def is_simple_design_template(template_name):
    return template_name in {'simple_pattern', 'simple_image', 'simple_retro'}


def _is_valid_hex_color(value):
    if not value or not isinstance(value, str):
        return False

    value = value.strip()
    if len(value) != 7 or not value.startswith('#'):
        return False

    allowed = set('0123456789abcdefABCDEF')
    return all(char in allowed for char in value[1:])


def _normalize_design_customization_item(raw_item, default_item, template_name=None):
    item = default_item.copy()
    if not isinstance(raw_item, dict):
        return item

    for key in ('blog_title_font', 'post_title_font', 'box_title_font', 'body_font'):
        font_key = raw_item.get(key)
        if font_key in DESIGN_FONT_STACKS:
            item[key] = font_key

    for key, min_value, max_value in (
        ('blog_title_size', 32, 96),
        ('post_title_size', 22, 64),
        ('box_title_size', 10, 28),
        ('post_date_size', 70, 170),
    ):
        size_value = str(raw_item.get(key, '')).strip()
        if size_value.isdigit():
            size_int = int(size_value)
            if min_value <= size_int <= max_value:
                item[key] = str(size_int)

    legacy_title_sizes = {
        'blog_title_size': ('54', str(default_item.get('blog_title_size', '32'))),
        'post_title_size': ('32', str(default_item.get('post_title_size', '24'))),
        'box_title_size': ('24', str(default_item.get('box_title_size', '13'))),
    }
    for field_name, (legacy_value, replacement_value) in legacy_title_sizes.items():
        if str(item.get(field_name, '')).strip() == legacy_value:
            item[field_name] = replacement_value

    for key in (
        'blog_title_color',
        'post_title_color',
        'box_title_color',
        'post_date_color',
        'post_date_color_1',
        'post_date_color_2',
        'body_text_color',
        'outer_background_color_1',
        'outer_background_color_2',
        'header_background_color_1',
        'header_background_color_2',
        'content_background_color',
        'content_border_color',
        'box_background_color',
        'box_border_color',
    ):
        color_value = raw_item.get(key)
        if _is_valid_hex_color(color_value):
            item[key] = color_value.strip()

    legacy_post_date_color = raw_item.get('post_date_color')
    if _is_valid_hex_color(legacy_post_date_color) and not _is_valid_hex_color(raw_item.get('post_date_color_1')):
        item['post_date_color_1'] = legacy_post_date_color.strip()
        item['post_date_color'] = legacy_post_date_color.strip()

    post_date_style = str(raw_item.get('post_date_style', '')).strip()
    if post_date_style in POST_DATE_STYLE_OPTIONS:
        item['post_date_style'] = post_date_style

    post_date_effect = str(raw_item.get('post_date_effect', '')).strip()
    if post_date_effect in POST_DATE_EFFECT_OPTIONS:
        item['post_date_effect'] = post_date_effect

    right_box_columns = str(raw_item.get('right_box_columns', '')).strip()
    if right_box_columns in {'1', '2'}:
        item['right_box_columns'] = right_box_columns

    outer_mode = str(raw_item.get('outer_background_mode', '')).strip()
    allowed_outer_modes = set(DESIGN_BACKGROUND_MODES)
    if default_item.get('outer_background_mode') == 'pattern' or template_name == 'simple_retro':
        allowed_outer_modes = {'color', 'gradient', 'pattern'}
    elif default_item.get('outer_background_mode') == 'system_image':
        allowed_outer_modes = {'color', 'system_image', 'upload_image'}

    if outer_mode in allowed_outer_modes:
        item['outer_background_mode'] = outer_mode

    header_mode = str(raw_item.get('header_background_mode', '')).strip()
    if header_mode in {'color', 'gradient'}:
        item['header_background_mode'] = header_mode

    outer_pattern = str(raw_item.get('outer_background_pattern', '')).strip()
    if outer_pattern in DESIGN_PATTERN_ASSETS:
        item['outer_background_pattern'] = outer_pattern

    outer_image = str(raw_item.get('outer_background_image', '')).strip()
    if outer_image in ALL_DESIGN_BACKGROUND_IMAGE_ASSETS:
        item['outer_background_image'] = outer_image

    for key in ('outer_background_gradient_direction', 'header_background_gradient_direction'):
        direction = str(raw_item.get(key, '')).strip()
        if direction in DESIGN_GRADIENT_DIRECTIONS:
            item[key] = direction

    return item


def get_default_design_customizations():
    return {
        template_name: values.copy()
        for template_name, values in DEFAULT_DESIGN_CUSTOMIZATIONS.items()
    }


def normalize_design_customizations(raw_customizations):
    defaults = get_default_design_customizations()
    if not isinstance(raw_customizations, dict):
        return defaults

    normalized = {}
    for template_name, default_values in defaults.items():
        normalized[template_name] = _normalize_design_customization_item(
            raw_customizations.get(template_name),
            default_values,
            template_name,
        )

    return normalized


def build_design_customization_payload(customization):
    payload = (customization or {}).copy()
    payload['blog_title_font_stack'] = DESIGN_FONT_STACKS.get(
        payload.get('blog_title_font'),
        DESIGN_FONT_STACKS['georgia'],
    )
    payload['post_title_font_stack'] = DESIGN_FONT_STACKS.get(
        payload.get('post_title_font'),
        DESIGN_FONT_STACKS['georgia'],
    )
    payload['box_title_font_stack'] = DESIGN_FONT_STACKS.get(
        payload.get('box_title_font'),
        DESIGN_FONT_STACKS['georgia'],
    )
    payload['body_font_stack'] = DESIGN_FONT_STACKS.get(
        payload.get('body_font'),
        DESIGN_FONT_STACKS['arial'],
    )
    payload['blog_title_size'] = str(payload.get('blog_title_size') or '32')
    payload['post_title_size'] = str(payload.get('post_title_size') or '24')
    payload['box_title_size'] = str(payload.get('box_title_size') or '13')
    payload['post_date_style'] = str(payload.get('post_date_style') or 'classic_vertical')
    if payload['post_date_style'] not in POST_DATE_STYLE_OPTIONS:
        payload['post_date_style'] = 'classic_vertical'

    payload['post_date_effect'] = str(payload.get('post_date_effect') or 'solid')
    if payload['post_date_effect'] not in POST_DATE_EFFECT_OPTIONS:
        payload['post_date_effect'] = 'solid'

    payload['post_date_color_1'] = payload.get('post_date_color_1') or payload.get('post_date_color') or '#d97706'
    payload['post_date_color_2'] = payload.get('post_date_color_2') or payload['post_date_color_1']
    payload['post_date_color'] = payload['post_date_color_1']
    payload['post_date_size'] = str(payload.get('post_date_size') or '100')
    if not payload['post_date_size'].isdigit() or not (70 <= int(payload['post_date_size']) <= 170):
        payload['post_date_size'] = '100'

    payload['right_box_columns'] = str(payload.get('right_box_columns') or '1')
    if payload['right_box_columns'] not in {'1', '2'}:
        payload['right_box_columns'] = '1'
    payload['outer_background_asset'] = DESIGN_PATTERN_ASSETS.get(
        payload.get('outer_background_pattern')
    )
    if payload.get('outer_background_mode') == 'system_image':
        payload['outer_background_asset'] = ALL_DESIGN_BACKGROUND_IMAGE_ASSETS.get(
            payload.get('outer_background_image')
        )
    payload['outer_background_mode'] = payload.get('outer_background_mode') or 'color'
    payload['header_background_mode'] = payload.get('header_background_mode') or 'color'
    return payload


def get_post_publication_datetime(post):
    dt = post.publish_at or post.created_at
    if not dt:
        return None
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt, timezone.get_current_timezone())
    return timezone.localtime(dt)


def annotate_publication_datetime(queryset, alias='publication_datetime_db'):
    return queryset.annotate(**{alias: Coalesce('publish_at', 'created_at')})


HOME_FEATURED_SLOT_SCHEDULE = (
    ("morning", 9),
    ("afternoon", 15),
    ("evening", 21),
)


def _get_home_featured_slot_datetime(slot_date, hour):
    return timezone.make_aware(
        datetime.combine(slot_date, time(hour=hour, minute=0)),
        timezone.get_current_timezone(),
    )


def _get_home_featured_day_bounds(target_date):
    start = timezone.make_aware(
        datetime.combine(target_date, time.min),
        timezone.get_current_timezone(),
    )
    end = start + timezone.timedelta(days=1)
    return start, end


def _get_home_featured_daily_cap(window_post_count):
    if window_post_count < 3:
        return 0
    if window_post_count < 9:
        return 1
    if window_post_count < 17:
        return 2
    return 3


def _get_desc_percentile_threshold(scores, ratio):
    if not scores:
        return 0
    ordered = sorted(scores, reverse=True)
    index = max(0, math.ceil(len(ordered) * ratio) - 1)
    return ordered[index]


def _get_home_featured_premium_filter():
    return (
        Q(author__profile__is_premium=True)
        | Q(
            author__profile__premium_until__isnull=False,
            publication_datetime_db__lte=F('author__profile__premium_until'),
        )
    )


def _user_has_active_premium(user, reference_dt=None):
    if not user:
        return False

    profile = getattr(user, 'profile', None)
    if not profile:
        return False

    if reference_dt is None:
        return bool(profile.has_active_premium)

    if getattr(profile, 'is_premium', False):
        return True

    premium_until = getattr(profile, 'premium_until', None)
    if not premium_until:
        return False

    if timezone.is_naive(reference_dt):
        reference_dt = timezone.make_aware(reference_dt, timezone.get_current_timezone())
    if timezone.is_naive(premium_until):
        premium_until = timezone.make_aware(premium_until, timezone.get_current_timezone())

    return premium_until >= reference_dt


def _get_home_featured_priority_source(user, reference_dt=None):
    if not user:
        return None
    if getattr(user, 'is_superuser', False) or getattr(user, 'is_staff', False):
        return 'admin'
    if _user_has_active_premium(user, reference_dt=reference_dt):
        return 'premium'
    return None


def _scaled_home_featured_ratio(value, baseline, baseline_floor=1.0, cap=5.0):
    value = max(float(value or 0), 0.0)
    baseline = max(float(baseline or 0), baseline_floor)
    denominator = math.log1p(baseline)
    if denominator <= 0:
        denominator = 1.0
    return min(math.log1p(value) / denominator, cap)


def _build_home_featured_candidates(base_queryset, slot_dt, excluded_post_ids=None, excluded_author_ids=None):
    excluded_post_ids = excluded_post_ids or set()
    excluded_author_ids = excluded_author_ids or set()

    window_start = slot_dt - timezone.timedelta(hours=24)
    recent_posts = list(
        annotate_publication_datetime(base_queryset)
        .filter(publication_datetime_db__gte=window_start, publication_datetime_db__lte=slot_dt)
        .exclude(
            Q(author__is_staff=True)
            | Q(author__is_superuser=True)
            | _get_home_featured_premium_filter()
        )
        .annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True),
            comment_authors_count=Count('comments__author', distinct=True),
        )
        .select_related('author', 'author__profile', 'category')
        .prefetch_related('images', 'tags')
        .order_by('-publication_datetime_db', '-created_at')
        .distinct()
    )

    all_recent_count = len(recent_posts)
    candidates = []
    seen_authors = set()

    for post in recent_posts:
        if post.id in excluded_post_ids:
            continue
        if post.author_id in excluded_author_ids:
            continue
        if post.author_id in seen_authors:
            continue

        publication_dt = getattr(post, 'publication_datetime_db', None) or post.publish_at or post.created_at
        if publication_dt is None:
            continue
        if timezone.is_naive(publication_dt):
            publication_dt = timezone.make_aware(publication_dt, timezone.get_current_timezone())

        post.home_featured_publication_datetime = timezone.localtime(publication_dt)
        post.home_featured_likes_count = getattr(post, 'likes_count', 0) or 0
        post.home_featured_comments_count = getattr(post, 'comments_count', 0) or 0
        post.home_featured_comment_authors_count = getattr(post, 'comment_authors_count', 0) or 0
        post.home_featured_engaged_users = post.home_featured_likes_count + post.home_featured_comment_authors_count
        post.home_featured_interaction_total = (
            post.home_featured_likes_count
            + (post.home_featured_comments_count * 2)
            + post.home_featured_engaged_users
        )
        post.home_featured_engagement_rate = (
            post.home_featured_likes_count
            + (post.home_featured_comments_count * 2.5)
            + (post.home_featured_engaged_users * 1.5)
        ) / max((post.views or 0), 15)
        candidates.append(post)
        seen_authors.add(post.author_id)

    if not candidates:
        return all_recent_count, []

    median_views = median([(post.views or 0) for post in candidates])
    median_likes = median([post.home_featured_likes_count for post in candidates])
    median_comments = median([post.home_featured_comments_count for post in candidates])
    median_engaged_users = median([post.home_featured_engaged_users for post in candidates])
    median_interaction_total = median([post.home_featured_interaction_total for post in candidates])
    median_engagement_rate = median([post.home_featured_engagement_rate for post in candidates])

    for post in candidates:
        publication_dt = getattr(post, 'home_featured_publication_datetime', None) or timezone.localtime(slot_dt)
        hours_since_publish = max((slot_dt - publication_dt).total_seconds() / 3600, 0)

        views_component = _scaled_home_featured_ratio(post.views or 0, median_views, baseline_floor=3.0, cap=4.0)
        likes_component = _scaled_home_featured_ratio(post.home_featured_likes_count, median_likes, baseline_floor=1.0, cap=5.5)
        comments_component = _scaled_home_featured_ratio(post.home_featured_comments_count, median_comments, baseline_floor=1.0, cap=6.0)
        engaged_component = _scaled_home_featured_ratio(post.home_featured_engaged_users, median_engaged_users, baseline_floor=1.0, cap=5.0)
        interaction_component = _scaled_home_featured_ratio(post.home_featured_interaction_total, median_interaction_total, baseline_floor=2.0, cap=6.0)
        engagement_component = min(
            float(post.home_featured_engagement_rate or 0) / max(float(median_engagement_rate or 0), 0.08),
            5.0,
        )

        raw_score = (
            (views_component * 0.08)
            + (likes_component * 0.24)
            + (comments_component * 0.26)
            + (engaged_component * 0.18)
            + (interaction_component * 0.16)
            + (engagement_component * 0.08)
        )
        adjusted_score = raw_score / math.sqrt(hours_since_publish + 1.5)

        post.home_featured_raw_score = round(raw_score, 4)
        post.home_featured_score = round(adjusted_score, 4)

    return all_recent_count, candidates


def _publish_priority_home_featured_posts(base_queryset, now=None, backfill_days=3):
    now = now or timezone.now()
    window_start = now - timezone.timedelta(days=backfill_days)
    featured_post_ids = set(
        HomeFeaturedPost.objects.exclude(post__isnull=True).values_list('post_id', flat=True)
    )

    priority_posts = (
        annotate_publication_datetime(base_queryset)
        .filter(publication_datetime_db__gte=window_start, publication_datetime_db__lte=now)
        .filter(
            Q(author__is_staff=True)
            | Q(author__is_superuser=True)
            | _get_home_featured_premium_filter()
        )
        .exclude(id__in=featured_post_ids)
        .select_related('author', 'author__profile')
        .order_by('publication_datetime_db', 'created_at')
        .distinct()
    )

    for post in priority_posts:
        source = _get_home_featured_priority_source(post.author, reference_dt=getattr(post, 'publication_datetime_db', None) or post.publish_at or post.created_at or now)
        if not source:
            continue
        featured_at = getattr(post, 'publication_datetime_db', None) or post.publish_at or post.created_at or now
        if timezone.is_naive(featured_at):
            featured_at = timezone.make_aware(featured_at, timezone.get_current_timezone())
        HomeFeaturedPost.objects.create(
            post=post,
            source=source,
            featured_at=featured_at,
            slot_date=timezone.localtime(featured_at).date(),
        )


def _pick_home_featured_post_for_slot(base_queryset, slot_dt, slot_name, slot_token):
    local_slot_dt = timezone.localtime(slot_dt)
    slot_date = local_slot_dt.date()
    day_start, day_end = _get_home_featured_day_bounds(slot_date)

    existing_today_entries = list(
        HomeFeaturedPost.objects.filter(
            source='algorithm',
            featured_at__gte=day_start,
            featured_at__lt=day_end,
            post__isnull=False,
        ).order_by('featured_at')
    )

    all_recent_count, candidates = _build_home_featured_candidates(
        base_queryset,
        slot_dt,
        excluded_post_ids=set(HomeFeaturedPost.objects.exclude(post__isnull=True).values_list('post_id', flat=True)),
        excluded_author_ids=set(
            HomeFeaturedPost.objects.filter(
                source='algorithm',
                featured_at__gte=slot_dt - timezone.timedelta(hours=48),
                featured_at__lt=slot_dt,
                post__isnull=False,
            ).values_list('post__author_id', flat=True)
        ),
    )

    daily_cap = _get_home_featured_daily_cap(all_recent_count)
    if daily_cap <= len(existing_today_entries):
        HomeFeaturedPost.objects.create(
            post=None,
            source='algorithm',
            featured_at=slot_dt,
            slot_date=slot_date,
            slot_name=slot_name,
            slot_token=slot_token,
        )
        return None

    if not candidates:
        HomeFeaturedPost.objects.create(
            post=None,
            source='algorithm',
            featured_at=slot_dt,
            slot_date=slot_date,
            slot_name=slot_name,
            slot_token=slot_token,
        )
        return None

    score_values = [getattr(post, 'home_featured_score', 0) or 0 for post in candidates]
    interaction_values = [getattr(post, 'home_featured_interaction_total', 0) or 0 for post in candidates]
    median_score = median(score_values) if score_values else 0
    median_interaction = median(interaction_values) if interaction_values else 0
    top_decile_threshold = _get_desc_percentile_threshold(score_values, 0.10)
    upper_third_threshold = _get_desc_percentile_threshold(score_values, 0.34)
    dynamic_threshold = max(median_score * 1.85, upper_third_threshold * 1.15)

    qualified = []
    for post in candidates:
        interaction_total = getattr(post, 'home_featured_interaction_total', 0) or 0
        score = getattr(post, 'home_featured_score', 0) or 0
        has_real_community_signal = interaction_total > max(0, median_interaction)
        if not has_real_community_signal:
            continue
        if score < top_decile_threshold:
            continue
        if score < dynamic_threshold:
            continue
        qualified.append(post)

    if existing_today_entries:
        previous_score = existing_today_entries[-1].score or 0
        qualified = [
            post for post in qualified
            if previous_score <= 0 or (getattr(post, 'home_featured_score', 0) or 0) >= previous_score * 0.90
        ]

    qualified.sort(
        key=lambda post: (
            getattr(post, 'home_featured_score', 0) or 0,
            getattr(post, 'home_featured_raw_score', 0) or 0,
            getattr(post, 'home_featured_publication_datetime', local_slot_dt),
        ),
        reverse=True,
    )

    chosen = qualified[0] if qualified else None
    HomeFeaturedPost.objects.create(
        post=chosen,
        source='algorithm',
        featured_at=slot_dt,
        slot_date=slot_date,
        slot_name=slot_name,
        slot_token=slot_token,
        score=getattr(chosen, 'home_featured_score', None) if chosen else None,
        raw_score=getattr(chosen, 'home_featured_raw_score', None) if chosen else None,
    )
    return chosen


def publish_due_home_featured_posts(now=None, backfill_days=3):
    now = now or timezone.now()
    base_queryset = Post.objects.filter(status='published')

    _publish_priority_home_featured_posts(base_queryset, now=now, backfill_days=backfill_days)

    local_today = timezone.localtime(now).date()
    start_date = local_today - timezone.timedelta(days=backfill_days)

    slot_dates = []
    cursor = start_date
    while cursor <= local_today:
        slot_dates.append(cursor)
        cursor += timezone.timedelta(days=1)

    existing_tokens = set(
        HomeFeaturedPost.objects.exclude(slot_token__isnull=True).values_list('slot_token', flat=True)
    )

    for slot_date in slot_dates:
        for slot_name, hour in HOME_FEATURED_SLOT_SCHEDULE:
            slot_dt = _get_home_featured_slot_datetime(slot_date, hour)
            if slot_dt > now:
                continue
            slot_token = f"{slot_date.isoformat()}:{slot_name}"
            if slot_token in existing_tokens:
                continue
            _pick_home_featured_post_for_slot(base_queryset, slot_dt, slot_name, slot_token)
            existing_tokens.add(slot_token)


def get_home_featured_posts(base_queryset, now=None):
    now = now or timezone.now()
    base_queryset = annotate_publication_datetime(base_queryset)

    entries = (
        HomeFeaturedPost.objects.filter(
            featured_at__lte=now,
            post__isnull=False,
            post__in=base_queryset,
        )
        .select_related('post', 'post__author', 'post__author__profile', 'post__category')
        .prefetch_related('post__images', 'post__tags')
        .order_by('-featured_at', '-created_at')
    )

    posts = []
    for entry in entries:
        post = entry.post
        post.home_featured_source = entry.source
        post.home_featured_at = timezone.localtime(entry.featured_at)
        post.home_featured_score = entry.score
        post.home_featured_raw_score = entry.raw_score
        posts.append(post)
    return posts

def _normalize_category_text(value):
    if not value:
        return ''

    value = str(value).strip().lower()
    value = value.replace('&', ' i ')
    value = value.replace('_', ' ')
    value = value.replace('-', ' ')
    value = value.replace('/', ' ')
    value = ' '.join(value.split())
    value = ''.join(
        char for char in unicodedata.normalize('NFKD', value)
        if not unicodedata.combining(char)
    )
    return value


CATEGORY_FOLDER_ALIASES = {
    'price': 'kultura_kreativnost/price',
    'prica': 'kultura_kreativnost/price',
    'price prica': 'kultura_kreativnost/price',
    'prica price': 'kultura_kreativnost/price',
    'zivotinje': 'priroda/zivotinje',
    'zivotinja': 'priroda/zivotinje',
    'kazaliste': 'kultura_kreativnost/Kazaliste',
    'pejzaz': 'priroda/pejzaz',
    'filmovi i serije': 'kultura_kreativnost/film_serije',
    'filmovi serije': 'kultura_kreativnost/film_serije',
    'film serije': 'kultura_kreativnost/film_serije',
    'rezencije': 'razno/recenzije',
    'recenzije': 'razno/recenzije',
    'putovanja': 'razno/putovanje',
    'putovanje': 'razno/putovanje',
}


def resolve_category_folder(category):
    if not category:
        return None

    normalized_map = {
        _normalize_category_text(key): value
        for key, value in CATEGORY_FOLDER_MAP.items()
    }

    candidates = []
    for raw_value in (getattr(category, 'name', None), getattr(category, 'slug', None)):
        if not raw_value:
            continue
        candidates.append(raw_value)
        normalized_value = _normalize_category_text(raw_value)
        if normalized_value:
            candidates.append(normalized_value)
            alias_value = CATEGORY_FOLDER_ALIASES.get(normalized_value)
            if alias_value:
                return alias_value

    for candidate in candidates:
        if candidate in CATEGORY_FOLDER_MAP:
            return CATEGORY_FOLDER_MAP[candidate]

        normalized_candidate = _normalize_category_text(candidate)
        if normalized_candidate in normalized_map:
            return normalized_map[normalized_candidate]

        alias_value = CATEGORY_FOLDER_ALIASES.get(normalized_candidate)
        if alias_value:
            return alias_value

    return None


def ensure_post_home_image(post, save=False):
    if not post or not getattr(post, 'category', None) or getattr(post, 'home_image', None):
        return False

    assign_home_image(post)
    if post.home_image and save and getattr(post, 'pk', None):
        post.save(update_fields=['home_image'])
    return bool(post.home_image)


def _read_comment_settings():
    try:
        if os.path.exists(COMMENT_SETTINGS_FILE):
            with open(COMMENT_SETTINGS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
    except Exception:
        pass
    return {}


def _write_comment_settings(data):
    os.makedirs(os.path.dirname(COMMENT_SETTINGS_FILE), exist_ok=True)
    with open(COMMENT_SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_allow_anonymous_comments(user):
    data = _read_comment_settings()
    return bool(data.get(str(user.id), False))


def set_allow_anonymous_comments(user, value):
    data = _read_comment_settings()
    data[str(user.id)] = bool(value)
    _write_comment_settings(data)


def _read_blog_preferences():
    try:
        if os.path.exists(BLOG_PREFERENCES_FILE):
            with open(BLOG_PREFERENCES_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
    except Exception:
        pass
    return {}


def _write_blog_preferences(data):
    os.makedirs(os.path.dirname(BLOG_PREFERENCES_FILE), exist_ok=True)
    with open(BLOG_PREFERENCES_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_blog_preferences(user):
    data = _read_blog_preferences()
    raw = data.get(str(user.id), {})
    prefs = DEFAULT_BLOG_PREFERENCES.copy()
    if isinstance(raw, dict):
        prefs.update(raw)

    try:
        prefs['posts_per_page'] = int(prefs.get('posts_per_page', 5) or 5)
    except Exception:
        prefs['posts_per_page'] = 5

    if prefs['posts_per_page'] not in (5, 10, 15, 20):
        prefs['posts_per_page'] = 5

    prefs['show_post_tags'] = bool(prefs.get('show_post_tags', True))
    prefs['show_post_comments'] = bool(prefs.get('show_post_comments', True))
    prefs['allow_comments'] = bool(prefs.get('allow_comments', True))
    prefs['analytics_live_counter_enabled'] = bool(prefs.get('analytics_live_counter_enabled', False))
    prefs['analytics_map_enabled'] = bool(prefs.get('analytics_map_enabled', False))
    prefs['analytics_geo_enabled'] = bool(prefs.get('analytics_geo_enabled', False))
    prefs['analytics_active_pages_enabled'] = bool(prefs.get('analytics_active_pages_enabled', False))

    cursor_style = str(prefs.get('cursor_style', DEFAULT_CURSOR_STYLE) or DEFAULT_CURSOR_STYLE).strip()
    if cursor_style not in BLOG_CURSOR_VALUES:
        cursor_style = DEFAULT_CURSOR_STYLE
    prefs['cursor_style'] = cursor_style

    cursor_choice = get_cursor_choice(cursor_style)
    prefs['cursor_css'] = cursor_choice.get('cursor_css', 'auto')
    prefs['cursor_pointer_css'] = cursor_choice.get('pointer_cursor_css', prefs['cursor_css'])
    prefs['cursor_stylesheet_url'] = cursor_choice.get('cursor_stylesheet_url', '')

    cursor_effect = str(prefs.get('cursor_effect', 'none') or 'none').strip()
    if cursor_effect not in BLOG_CURSOR_EFFECT_VALUES:
        cursor_effect = 'none'
    prefs['cursor_effect'] = cursor_effect

    prefs['ambient_music_enabled'] = bool(prefs.get('ambient_music_enabled', False))

    raw_track_id = str(prefs.get('ambient_music_track', '') or '').strip()
    ambient_track = get_ambient_music_track(raw_track_id)
    if not ambient_track and prefs['ambient_music_enabled']:
        ambient_track = get_ambient_music_track(DEFAULT_AMBIENT_MUSIC_TRACK)
        raw_track_id = ambient_track['id'] if ambient_track else ''
    elif not ambient_track:
        raw_track_id = ''

    prefs['ambient_music_track'] = raw_track_id
    prefs['ambient_music_track_data'] = ambient_track

    try:
        ambient_music_volume = int(prefs.get('ambient_music_volume', 18) or 18)
    except Exception:
        ambient_music_volume = 18
    prefs['ambient_music_volume'] = max(0, min(100, ambient_music_volume))

    if prefs.get('blog_archive_mode') not in {'both', 'calendar', 'list', 'none'}:
        prefs['blog_archive_mode'] = 'both'

    widget_side = prefs.get('analytics_widget_side')
    if widget_side == 'left':
        widget_side = 'left_top'
    elif widget_side == 'right':
        widget_side = 'right_top'

    if widget_side not in {'left_top', 'left_bottom', 'right_top', 'right_bottom', 'footer_full'}:
        widget_side = 'right_top'

    prefs['analytics_widget_side'] = widget_side

    if prefs.get('analytics_map_variant') not in {'map', 'globe'}:
        prefs['analytics_map_variant'] = 'map'

    if prefs.get('analytics_stat_card_size') not in {'small', 'medium', 'large'}:
        prefs['analytics_stat_card_size'] = 'small'

    prefs['design_customizations'] = normalize_design_customizations(
        prefs.get('design_customizations')
    )

    active_template = getattr(getattr(user, 'profile', None), 'template', 'default')
    if active_template not in prefs['design_customizations']:
        active_template = 'default'

    active_design_customization = prefs['design_customizations'].get(active_template)
    if not active_design_customization:
        active_design_customization = prefs['design_customizations']['default']

    prefs['active_design_customization'] = build_design_customization_payload(
        active_design_customization
    )

    return prefs


def set_blog_preferences(user, preferences):
    current = get_blog_preferences(user)
    current.update(preferences or {})
    current['design_customizations'] = normalize_design_customizations(
        current.get('design_customizations')
    )
    current.pop('active_design_customization', None)
    data = _read_blog_preferences()
    data[str(user.id)] = current
    _write_blog_preferences(data)
    return current


def apply_blog_preferences_to_profile(profile, user=None):
    user = user or getattr(profile, 'user', None)
    if not user:
        return DEFAULT_BLOG_PREFERENCES.copy()

    prefs = get_blog_preferences(user)
    profile.posts_per_page = prefs['posts_per_page']
    profile.show_post_tags = prefs['show_post_tags']
    profile.show_post_comments = prefs['show_post_comments']
    profile.allow_comments = prefs['allow_comments']
    profile.blog_archive_mode = prefs['blog_archive_mode']
    return prefs


def apply_blog_preferences_to_posts(posts):
    for post in posts:
        if hasattr(post, 'author') and hasattr(post.author, 'profile'):
            apply_blog_preferences_to_profile(post.author.profile, post.author)
        ensure_post_home_image(post, save=True)


def apply_tags_to_post(post, tag_names):
    tags = []
    for name in tag_names:
        tag, _ = Tag.objects.get_or_create(name=name)
        tags.append(tag)
    post.tags.set(tags)


def publish_due_posts(author=None):
    due_posts = Post.objects.filter(
        status='scheduled',
        publish_at__isnull=False,
        publish_at__lte=timezone.now(),
    ).select_related('category')

    if author is not None:
        due_posts = due_posts.filter(author=author)

    for post in due_posts:
        post.status = 'published'
        assign_home_image(post)
        update_fields = ['status']
        if post.home_image:
            update_fields.append('home_image')
        post.save(update_fields=update_fields)


def enrich_posts_with_quiz_poll_data(posts, request_user):
    is_auth = request_user.is_authenticated

    for post in posts:
        post.quiz_user_answer = None
        post.quiz_is_correct = None
        post.poll_user_vote = None
        post.poll_results = []
        post.poll_total = 0
        apply_blog_preferences_to_profile(post.author.profile, post.author)
        post.allow_anonymous_comments = get_allow_anonymous_comments(post.author)
        ensure_post_home_image(post, save=True)

        if post.post_type == 'quiz':
            if is_auth:
                ans = QuizAnswer.objects.filter(post=post, user=request_user).select_related('selected_option').first()
                post.quiz_user_answer = ans
                if ans:
                    post.quiz_is_correct = ans.selected_option.is_correct

        elif post.post_type == 'poll':
            post.poll_total = PollVote.objects.filter(post=post).count()
            if is_auth:
                post.poll_user_vote = PollVote.objects.filter(post=post, user=request_user).select_related('option').first()

            results = []
            for opt in post.poll_options.all():
                count = PollVote.objects.filter(post=post, option=opt).count()
                percent = round((count / post.poll_total) * 100) if post.poll_total > 0 else 0
                results.append({
                    'id': opt.id,
                    'text': opt.text,
                    'count': count,
                    'percent': percent,
                })
            post.poll_results = results



def build_archives_for_user(user):
    publish_due_posts(user)
    tz = timezone.get_current_timezone()
    qs = (
        annotate_publication_datetime(
            Post.objects.filter(
                author=user,
                status='published',
            )
        )
        .filter(publication_datetime_db__lte=timezone.now())
        .annotate(m=TruncMonth('publication_datetime_db', tzinfo=tz))
        .values('m')
        .annotate(count=Count('id'))
        .order_by('-m')
    )

    archives = []
    for row in qs:
        month_date = row['m']
        if not month_date:
            continue
        archives.append({
            'year': month_date.year,
            'month': month_date.month,
            'label': f"{MONTHS_HR.get(month_date.month, '')}, {month_date.year}.",
            'count': row['count'],
        })
    return archives



def build_calendar_for_user(user, year, month):
    publish_due_posts(user)
    month_cal = calendar.monthcalendar(year, month)
    tz = timezone.get_current_timezone()

    start_local = timezone.datetime(year, month, 1, 0, 0, 0)
    if month == 12:
        end_local = timezone.datetime(year + 1, 1, 1, 0, 0, 0)
    else:
        end_local = timezone.datetime(year, month + 1, 1, 0, 0, 0)

    start_dt = timezone.make_aware(start_local, tz)
    end_dt = timezone.make_aware(end_local, tz)

    posts = (
        annotate_publication_datetime(
            Post.objects.filter(
                author=user,
                status='published',
            )
        )
        .filter(
            publication_datetime_db__gte=start_dt,
            publication_datetime_db__lt=end_dt,
            publication_datetime_db__lte=timezone.now(),
        )
        .only('id', 'created_at', 'publish_at')
        .order_by('publication_datetime_db', 'created_at')
    )

    day_map = {}
    for post in posts:
        local_publication_datetime = get_post_publication_datetime(post)
        if not local_publication_datetime:
            continue
        day_map.setdefault(local_publication_datetime.day, []).append(post.id)

    days_with_posts = sorted(day_map.keys())
    day_single_post_map = {day: ids[0] if len(ids) == 1 else None for day, ids in day_map.items()}
    return month_cal, days_with_posts, day_single_post_map




def get_adjacent_month(year, month, step):
    if step not in {-1, 1}:
        raise ValueError('step must be -1 or 1')

    if step == -1:
        if month == 1:
            return year - 1, 12
        return year, month - 1

    if month == 12:
        return year + 1, 1
    return year, month + 1


def build_month_navigation_urls(base_url, year, month, extra_params=None):
    params = {key: value for key, value in (extra_params or {}).items() if value not in (None, '')}

    prev_year, prev_month = get_adjacent_month(year, month, -1)
    next_year, next_month = get_adjacent_month(year, month, 1)

    def make_url(target_year, target_month):
        query = params.copy()
        query['year'] = target_year
        query['month'] = target_month
        return f"{base_url}?{urlencode(query)}"

    return make_url(prev_year, prev_month), make_url(next_year, next_month)

def get_active_category_name(category_slug):
    if not category_slug:
        return None
    category = Category.objects.filter(slug=category_slug).only('name').first()
    return category.name if category else None


def build_author_profile_items(profile):
    items = []

    def add(label, value):
        if value in (None, ''):
            return
        if isinstance(value, str):
            value = value.strip()
            if not value:
                return
        items.append({'label': label, 'value': value})

    add('Ime i prezime', getattr(profile, 'author_full_name', ''))
    add('Nadimak', getattr(profile, 'author_nickname', ''))
    add('Datum rođenja', profile.author_birth_date.strftime('%d.%m.%Y.') if getattr(profile, 'author_birth_date', None) else None)
    add('Mjesto rođenja', getattr(profile, 'author_birth_place', ''))
    add('Obrazovanje', getattr(profile, 'author_education', ''))
    add('Zanimanje / posao', getattr(profile, 'author_occupation', ''))
    add('Jezici', getattr(profile, 'author_languages', ''))
    add('Religija', getattr(profile, 'author_religion', ''))
    add('Nacionalnost', getattr(profile, 'author_nationality', ''))
    add('Hobiji', getattr(profile, 'author_hobbies', ''))
    add('Interesi', getattr(profile, 'author_interests', ''))
    add('Omiljene teme o kojima piše', getattr(profile, 'author_favorite_topics', ''))
    add('Što ga inspirira', getattr(profile, 'author_inspiration', ''))
    add('Moto', getattr(profile, 'author_motto', ''))
    add('Kontakt', getattr(profile, 'author_contact', ''))
    add('Društvene mreže', getattr(profile, 'author_social_links', ''))
    add('Web stranica / portfolio', getattr(profile, 'author_website', ''))

    return items


def build_author_profile_sections(profile):
    def clean(value):
        if value is None:
            return ''
        if isinstance(value, str):
            return value.strip()
        return value

    def item(label, value):
        value = clean(value)
        if not value:
            return None
        return {'label': label, 'value': value}

    osobno = [
        item('Ime i prezime', getattr(profile, 'author_full_name', '')),
        item('Nadimak', getattr(profile, 'author_nickname', '')),
        item('Datum rođenja', profile.author_birth_date.strftime('%d.%m.%Y.') if getattr(profile, 'author_birth_date', None) else None),
        item('Mjesto rođenja', getattr(profile, 'author_birth_place', '')),
        item('Obrazovanje', getattr(profile, 'author_education', '')),
        item('Zanimanje / posao', getattr(profile, 'author_occupation', '')),
        item('Jezici', getattr(profile, 'author_languages', '')),
        item('Religija', getattr(profile, 'author_religion', '')),
        item('Nacionalnost', getattr(profile, 'author_nationality', '')),
    ]

    interesi = [
        item('Hobiji', getattr(profile, 'author_hobbies', '')),
        item('Interesi', getattr(profile, 'author_interests', '')),
        item('Omiljene teme o kojima piše', getattr(profile, 'author_favorite_topics', '')),
        item('Što ga inspirira', getattr(profile, 'author_inspiration', '')),
        item('Moto', getattr(profile, 'author_motto', '')),
    ]

    poveznice = [
        item('Kontakt', getattr(profile, 'author_contact', '')),
        item('Društvene mreže', getattr(profile, 'author_social_links', '')),
        item('Web stranica / portfolio', getattr(profile, 'author_website', '')),
    ]

    sections = []
    for title, section_items in [
        ('Osobno i identitet', osobno),
        ('Interesi i pisanje', interesi),
        ('Poveznice i kontakt', poveznice),
    ]:
        filtered = [x for x in section_items if x]
        if filtered:
            sections.append({'title': title, 'items': filtered})

    return sections


def has_public_author_content(profile):
    return bool(getattr(profile, 'has_author_content', False))


def get_public_author_questions(author):
    return (
        AuthorQuestion.objects
        .filter(author=author, is_public=True)
        .exclude(answer='')
        .select_related('sender')
    )


def get_private_author_questions_for_viewer(author, viewer):
    if not getattr(viewer, 'is_authenticated', False) or viewer == author:
        return AuthorQuestion.objects.none()

    return (
        AuthorQuestion.objects
        .filter(author=author, sender=viewer, is_public=False)
        .select_related('sender')
    )


def are_users_blocked(user_a, user_b):
    if not getattr(user_a, 'is_authenticated', False) or user_a == user_b:
        return False
    return (
        UserBlock.objects.filter(blocker=user_a, blocked=user_b).exists()
        or UserBlock.objects.filter(blocker=user_b, blocked=user_a).exists()
    )


def is_user_restricted(owner, user):
    if not getattr(user, "is_authenticated", False) or owner == user:
        return False
    return UserRestriction.objects.filter(owner=owner, restricted=user).exists()


def assign_home_image(post):
    if not post.category or post.home_image:
        return

    # 1) Prvo koristi slike koje administrator ubaci kroz Django admin.
    #    One se spremaju u MEDIA i vezane su uz kategoriju.
    uploaded_images = list(
        CategoryHomeImage.objects.filter(
            category=post.category,
            is_active=True,
        ).exclude(image="")
    )

    if uploaded_images:
        selected_uploaded = random.choice(uploaded_images)
        if selected_uploaded.image:
            post.home_image = selected_uploaded.image.url
            return

    # 2) Ako za kategoriju nema admin uploadanih slika, koristi stare static slike.
    folder = resolve_category_folder(post.category)
    if not folder:
        return

    folder_path = os.path.join(settings.BASE_DIR, 'blog', 'static', 'images', 'home', folder)
    if not os.path.exists(folder_path):
        return

    images = [name for name in os.listdir(folder_path) if name.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not images:
        return

    selected = random.choice(images)
    post.home_image = f'images/home/{folder}/{selected}'


def get_profile_user_or_404(username):
    from django.contrib.auth.models import User
    from django.shortcuts import get_object_or_404

    return get_object_or_404(User.objects.select_related('profile'), username=username)



def get_profile_posts_queryset(profile_user, request_user, category_slug=None, year=None, month=None, day=None):
    publish_due_posts(profile_user)
    tz = timezone.get_current_timezone()

    posts = annotate_publication_datetime(
        Post.objects.filter(
            author=profile_user,
            status='published',
        )
    ).filter(publication_datetime_db__lte=timezone.now())

    posts = (
        posts.select_related('author', 'author__profile', 'category')
        .prefetch_related('images', 'tags', 'quiz_options', 'poll_options', 'comments', 'likes')
        .order_by('-publication_datetime_db', '-created_at')
    )

    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    start_dt = None
    end_dt = None

    if year is not None and month is not None and day is not None:
        start_local = timezone.datetime(year, month, day, 0, 0, 0)
        end_local = start_local + timezone.timedelta(days=1)
        start_dt = timezone.make_aware(start_local, tz)
        end_dt = timezone.make_aware(end_local, tz)
    elif year is not None and month is not None:
        start_local = timezone.datetime(year, month, 1, 0, 0, 0)
        if month == 12:
            end_local = timezone.datetime(year + 1, 1, 1, 0, 0, 0)
        else:
            end_local = timezone.datetime(year, month + 1, 1, 0, 0, 0)
        start_dt = timezone.make_aware(start_local, tz)
        end_dt = timezone.make_aware(end_local, tz)
    elif year is not None:
        start_local = timezone.datetime(year, 1, 1, 0, 0, 0)
        end_local = timezone.datetime(year + 1, 1, 1, 0, 0, 0)
        start_dt = timezone.make_aware(start_local, tz)
        end_dt = timezone.make_aware(end_local, tz)

    if start_dt is not None and end_dt is not None:
        posts = posts.filter(publication_datetime_db__gte=start_dt, publication_datetime_db__lt=end_dt)

    return posts


def paginate_posts(posts, per_page, page_number):
    paginator = Paginator(posts, per_page)
    return paginator.get_page(page_number)


def prepare_blog_context(request, profile_user, template_name, category_slug=None, archive_base_url=None):
    publish_due_posts(profile_user)
    profile = profile_user.profile
    blog_preferences = apply_blog_preferences_to_profile(profile, profile_user)
    allow_anonymous_comments = get_allow_anonymous_comments(profile_user)

    today = timezone.localdate()

    year_param = request.GET.get('year')
    month_param = request.GET.get('month')
    day_param = request.GET.get('day')

    try:
        filter_year = int(year_param) if year_param else None
    except (TypeError, ValueError):
        filter_year = None

    try:
        filter_month = int(month_param) if month_param else None
    except (TypeError, ValueError):
        filter_month = None

    try:
        filter_day = int(day_param) if day_param else None
    except (TypeError, ValueError):
        filter_day = None

    display_year = filter_year if filter_year is not None else today.year
    display_month = filter_month if filter_month is not None else today.month
    current_day = today.day if display_year == today.year and display_month == today.month else None

    posts = get_profile_posts_queryset(
        profile_user,
        request.user,
        category_slug=category_slug,
        year=filter_year,
        month=filter_month,
        day=filter_day,
    )
    enrich_posts_with_quiz_poll_data(posts, request.user)

    page_obj = paginate_posts(posts, blog_preferences['posts_per_page'], request.GET.get('page'))
    current_posts = list(page_obj.object_list)

    for post in current_posts:
        post.allow_anonymous_comments = allow_anonymous_comments

    month_calendar, days_with_posts, day_single_post_map = build_calendar_for_user(
        profile_user,
        display_year,
        display_month,
    )
    archives = build_archives_for_user(profile_user)

    calendar_extra_params = {}
    for key in ('category', 'tag'):
        value = request.GET.get(key)
        if value:
            calendar_extra_params[key] = value

    prev_month_url, next_month_url = build_month_navigation_urls(
        archive_base_url or reverse('user_blog', args=[profile_user.username]),
        display_year,
        display_month,
        calendar_extra_params,
    )

    live_analytics = build_live_analytics_context(profile_user)
    analytics_tracking = build_tracking_context(profile_user, blog_preferences, page_label='blog')

    context = {
        'blog': profile_user,
        'page_obj': page_obj,
        'posts': current_posts,
        'left_boxes': UserBox.objects.filter(user=profile_user, position='left').order_by('order'),
        'right_boxes': UserBox.objects.filter(user=profile_user, position='right').order_by('order'),
        'month_calendar': month_calendar,
        'current_day': current_day,
        'current_month_num': display_month,
        'current_month_hr': MONTHS_HR.get(display_month, ''),
        'current_year': display_year,
        'days_with_posts': days_with_posts,
        'day_single_post_map': day_single_post_map,
        'archives': archives,
        'archive_base_url': archive_base_url or reverse('user_blog', args=[profile_user.username]),
        'prev_month_url': prev_month_url,
        'next_month_url': next_month_url,
        'active_category_slug': category_slug,
        'active_category_name': get_active_category_name(category_slug),
        'has_author_content': has_public_author_content(profile),
        'author_profile_items': build_author_profile_items(profile),
        'author_page_url': reverse('author_detail', args=[profile_user.username]),
        'is_following': request.user.is_authenticated and Follow.objects.filter(follower=request.user, following=profile_user).exists(),
        'is_restricted': is_user_restricted(profile_user, request.user),
        'followers_count': Follow.objects.filter(following=profile_user).count(),
        'following_count': Follow.objects.filter(follower=profile_user).count(),
        'allow_anonymous_comments': allow_anonymous_comments,
        'anonymous_comment_username': ANONYMOUS_COMMENT_USERNAME,
        'blog_preferences': blog_preferences,
        'form': CommentForm(),
        'is_detail': False,
        'live_analytics': live_analytics,
        'analytics_tracking': analytics_tracking,
    }

    return render(request, template_name, context)


def _pick_message_for_event(event, target_date):
    existing = SpecialDaySelection.objects.filter(
        event=event,
        selection_date=target_date
    ).select_related("message").first()

    if existing:
        return existing.message

    messages = list(event.messages.filter(is_active=True))
    if not messages:
        return None

    last_selection = event.selections.select_related("message").first()
    if last_selection and len(messages) > 1:
        filtered = [message for message in messages if message.id != last_selection.message_id]
        if filtered:
            messages = filtered

    chosen = random.choice(messages)
    SpecialDaySelection.objects.create(
        event=event,
        message=chosen,
        selection_date=target_date
    )
    return chosen


def get_special_day_cards(target_date=None):
    target_date = target_date or timezone.localdate()
    cards = {"top": None, "left": None, "right": None}

    events = list(
        SpecialDayEvent.objects.filter(is_active=True)
        .prefetch_related("messages")
        .order_by("priority", "id")
    )

    for event in events:
        if not event.matches_date(target_date):
            continue

        position = event.position or "top"
        if position not in cards or cards[position] is not None:
            continue

        chosen_message = _pick_message_for_event(event, target_date)
        if not chosen_message:
            continue

        cards[position] = {
            "event": event,
            "message": chosen_message,
            "theme": event.theme,
            "label": event.accent_label or event.name,
            "position": position,
            "date": target_date,
        }

        if all(cards[pos] is not None for pos in cards):
            break

    return cards


def get_blog_page_response(request, blog_user, template_name, allow_follow=True, archive_base_url=None):
    response = prepare_blog_context(
        request=request,
        profile_user=blog_user,
        template_name=template_name,
        category_slug=request.GET.get('category'),
        archive_base_url=archive_base_url,
    )
    return response
