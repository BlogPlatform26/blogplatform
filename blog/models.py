from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from urllib.parse import parse_qs, urlparse
import re
import os


def validate_image_size(image):
    max_mb = int(os.environ.get("MAX_IMAGE_UPLOAD_SIZE_MB", 5))
    max_bytes = max_mb * 1024 * 1024

    if image.size > max_bytes:
        raise ValidationError(f"Slika je prevelika (max {max_mb}MB).")

def extract_youtube_video_id(url):
    url = (url or "").strip()
    if not url:
        return ""

    try:
        parsed = urlparse(url)
    except Exception:
        return ""

    host = (parsed.netloc or "").lower()
    path = (parsed.path or "").strip("/")

    if host in {"youtu.be", "www.youtu.be"}:
        video_id = path.split("/")[0] if path else ""

    elif host in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
        if path == "watch":
            video_id = parse_qs(parsed.query).get("v", [""])[0]
        elif path.startswith("embed/"):
            parts = path.split("/")
            video_id = parts[1] if len(parts) > 1 else ""
        elif path.startswith("shorts/"):
            parts = path.split("/")
            video_id = parts[1] if len(parts) > 1 else ""
        elif path.startswith("live/"):
            parts = path.split("/")
            video_id = parts[1] if len(parts) > 1 else ""
        else:
            video_id = ""
    else:
        return ""

    if re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id or ""):
        return video_id

    return ""

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    GROUP_CHOICES = [
        ("znanje", "Znanost & Znanje"),
        ("zivot", "Život & Psihologija"),
        ("drustvo", "Društvo"),
        ("kultura", "Kultura & Kreativnost"),
        ("priroda", "Priroda"),
        ("razno", "Razno"),
    ]

    group = models.CharField(
        max_length=20,
        choices=GROUP_CHOICES,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class CategoryHomeImage(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="home_images"
    )
    title = models.CharField(max_length=120, blank=True, default="")
    image = models.ImageField(
        upload_to="category_home_images/",
        validators=[validate_image_size]
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category__group", "category__name", "-created_at"]
        verbose_name = "Slika za kategoriju"
        verbose_name_plural = "Slike za kategorije"

    def __str__(self):
        label = self.title or self.image.name
        return f"{self.category.name} - {label}"


# ✅ TAGOVI
class Tag(models.Model):
    # npr. "ljubav", "film_serije", "co2"
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = [
        ("published", "Objavljen"),
        ("draft", "Skica"),
        ("scheduled", "Na čekanju"),
        ("deleted", "Obrisan"),
    ]

    POST_TYPE_CHOICES = [
        ("post", "Post"),
        ("quiz", "Kviz"),
        ("poll", "Anketa"),
    ]

    title = models.CharField(max_length=200)
    content = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    image = models.ImageField(
        upload_to="post_images/",
        blank=True,
        null=True,
        validators=[validate_image_size]
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft"
    )

    allow_comments = models.BooleanField(default=True)
    publish_at = models.DateTimeField(blank=True, null=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts"
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="posts"
    )

    video_url = models.URLField(
        max_length=500,
        blank=True,
        null=True
    )

    home_image = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    post_type = models.CharField(
        max_length=10,
        choices=POST_TYPE_CHOICES,
        default="post"
    )

    def is_liked_by(self, user):
        if user.is_authenticated:
            return self.likes.filter(user=user).exists()
        return False

    @property
    def youtube_video_id(self):
        return extract_youtube_video_id(self.video_url)

    @property
    def youtube_embed_url(self):
        video_id = self.youtube_video_id
        if not video_id:
            return ""
        return f"https://www.youtube.com/embed/{video_id}"

    @property
    def publication_datetime(self):
        dt = self.publish_at or self.created_at
        if not dt:
            return None
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt, timezone.get_current_timezone())
        return timezone.localtime(dt)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    blog_name = models.CharField(max_length=200)
    blog_tagline = models.CharField(max_length=220, blank=True, default="")
    background_color = models.CharField(max_length=20, default="#ffffff")

    # 🔴 Novo polje – čeka potvrdu emaila
    pending_email = models.EmailField(blank=True, null=True)
    is_premium = models.BooleanField(default=False)
    premium_until = models.DateTimeField(blank=True, null=True)

    TEMPLATE_CHOICES = (
        ("default", "Default"),
        ("dark", "Dark"),
        ("classic", "Classic"),
        ("default_right", "Default Plus"),
        ("dark_right", "Dark Plus"),
        ("classic_right", "Classic Plus"),
        ("simple_pattern", "Simple Uzorak"),
        ("simple_image", "Simple Slika"),
        ("simple_retro", "Simple Retro"),
        ("soho", "Studio"),
        ("magazin", "Magazin"),
        ("litica_noci", "Litica u noći"),
        ("podvodna_tisina", "Podvodna tišina"),
        ("vodopad_u_magli", "Vodopad u magli"),
        ("planine_u_magli", "Planine u magli"),
        ("nebeski_mir", "Nebeski mir"),
        ("svemirski_horizont", "Svemirski horizont"),
        ("zlatni_horizont", "Zlatni horizont"),
        ("iznad_oblaka", "Iznad oblaka"),
        ("sumska_svjetlost", "Šumska svjetlost"),
        ("polarna_svjetlost", "Polarna svjetlost"),
        ("zlatno_polje", "Zlatno polje"),
        ("neonski_grad", "Neonski grad"),
        ("polje_lavande", "Polje lavande"),
        ("carobna_ljubicasta", "Čarobni sumrak"),
        ("kraljevska_pozornica", "Kraljevska pozornica"),
        ("dimni_akordi", "Dimni akordi"),
        ("nebeska_klasika", "Nebeska klasika"),
        ("ponocna_elegancija", "Ponoćna elegancija"),
        ("ruzicasti_vrt", "Ružičasti vrt"),
        ("stara_aleja", "Stara aleja"),
        ("staza_prema_vrhovima", "Staza prema vrhovima"),
        ("jedro_u_suton", "Jedro u suton"),
        ("misticno_jezero", "Mistična laguna"),
        ("sjene_ulice", "Sjene ulice"),
        ("mjesecev_ples", "Mjesečev ples"),
        ("asfaltni_plamen", "Asfaltni plamen"),
    )

    template = models.CharField(
        max_length=50,
        choices=TEMPLATE_CHOICES,
        default="default"
    )

    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        validators=[validate_image_size]
    )

    BLOG_BANNER_POSITION_CHOICES = (
        ("left", "Lijevo"),
        ("center", "Sredina"),
        ("right", "Desno"),
    )

    blog_banner = models.ImageField(
        upload_to="blog_banners/",
        blank=True,
        null=True,
        validators=[validate_image_size]
    )

    blog_banner_position = models.CharField(
        max_length=10,
        choices=BLOG_BANNER_POSITION_CHOICES,
        default="center"
    )

    simple_background_image = models.ImageField(
        upload_to="design_backgrounds/custom/",
        blank=True,
        null=True,
        validators=[validate_image_size]
    )

    SOHO_HERO_PRESET_CHOICES = (
        ("", "Bez sistemske slike"),
        ("bookshelf", "Police s knjigama"),
        ("cute_pets_flower", "Pas i mačka"),
        ("abstract_earth", "Apstraktni tonovi"),
        ("blue_tech", "Plava tehnologija"),
        ("dreamy_sunset", "Zamagljeni zalazak"),
        ("misty_mountains", "Maglovite planine"),
        ("night_camp", "Noćno kampiranje"),
        ("navy_coffee", "Kava i bilježnica"),
        ("watercolor_workspace", "Kreativni stol"),
    )

    soho_hero_image = models.ImageField(
        upload_to="blog_hero_images/",
        blank=True,
        null=True,
        validators=[validate_image_size]
    )

    soho_hero_preset = models.CharField(
        max_length=50,
        choices=SOHO_HERO_PRESET_CHOICES,
        blank=True,
        default=""
    )

    author_bio = models.TextField(blank=True, default="")
    author_full_name = models.CharField(max_length=180, blank=True, default="")
    author_nickname = models.CharField(max_length=120, blank=True, default="")
    author_birth_date = models.DateField(blank=True, null=True)
    author_birth_place = models.CharField(max_length=150, blank=True, default="")
    author_education = models.CharField(max_length=220, blank=True, default="")
    author_occupation = models.CharField(max_length=180, blank=True, default="")
    author_languages = models.CharField(max_length=220, blank=True, default="")
    author_religion = models.CharField(max_length=120, blank=True, default="")
    author_nationality = models.CharField(max_length=120, blank=True, default="")
    author_hobbies = models.CharField(max_length=220, blank=True, default="")
    author_interests = models.CharField(max_length=220, blank=True, default="")
    author_favorite_topics = models.CharField(max_length=220, blank=True, default="")
    author_inspiration = models.CharField(max_length=220, blank=True, default="")
    author_motto = models.CharField(max_length=220, blank=True, default="")
    author_contact = models.TextField(blank=True, default="")
    author_social_links = models.TextField(blank=True, default="")
    author_website = models.CharField(max_length=320, blank=True, default="")
    allow_author_questions = models.BooleanField(default=False)

    @property
    def has_author_content(self):
        return any([
            bool((self.author_bio or '').strip()),
            bool((self.author_full_name or '').strip()),
            bool((self.author_nickname or '').strip()),
            bool(self.author_birth_date),
            bool((self.author_birth_place or '').strip()),
            bool((self.author_education or '').strip()),
            bool((self.author_occupation or '').strip()),
            bool((self.author_languages or '').strip()),
            bool((self.author_religion or '').strip()),
            bool((self.author_nationality or '').strip()),
            bool((self.author_hobbies or '').strip()),
            bool((self.author_interests or '').strip()),
            bool((self.author_favorite_topics or '').strip()),
            bool((self.author_inspiration or '').strip()),
            bool((self.author_motto or '').strip()),
            bool((self.author_contact or '').strip()),
            bool((self.author_social_links or '').strip()),
            bool((self.author_website or '').strip()),
        ])

    @property
    def has_temporary_premium(self):
        premium_until = self.premium_until
        if not premium_until:
            return False
        if timezone.is_naive(premium_until):
            premium_until = timezone.make_aware(premium_until, timezone.get_current_timezone())
        return premium_until >= timezone.now()

    @property
    def has_active_premium(self):
        return bool(self.is_premium or self.has_temporary_premium)

    @property
    def premium_status_label(self):
        if self.is_premium and self.has_temporary_premium:
            return "Trajni + privremeni"
        if self.is_premium:
            return "Trajni"
        if self.has_temporary_premium:
            return "Privremeni"
        return "Nema"

    def __str__(self):
        return f"{self.user.username} profil"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class UserBox(models.Model):
    POSITION_CHOICES = (
        ("left", "Left"),
        ("right", "Right"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    position = models.CharField(max_length=10, choices=POSITION_CHOICES)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower} prati {self.following}"


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ("follow", "Follow"),
        ("like", "Like"),
        ("comment", "Comment"),
    )

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)

    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.recipient.username} - {self.notification_type}"


class AuthorQuestion(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_author_questions")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_author_questions")
    question = models.TextField()
    answer = models.TextField(blank=True, default="")
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    answered_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def is_answered(self):
        return bool((self.answer or '').strip())

    def __str__(self):
        return f"Pitanje za {self.author.username} od {self.sender.username}"


# ==========================================================
# ✅ KVIZ / ANKETA MODELI
# ==========================================================

class QuizOption(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="quiz_options")
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.post.id} - {self.text}"


class QuizAnswer(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="quiz_answers")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(QuizOption, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return f"{self.user.username} -> kviz {self.post.id}"


class PollOption(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="poll_options")
    text = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.post.id} - {self.text}"


class PollVote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="poll_votes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return f"{self.user.username} -> anketa {self.post.id}"


class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="post_images/", validators=[validate_image_size])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for post {self.post_id}"
    
class SiteMessage(models.Model):
    content_html = models.TextField(blank=True, default="")

    image = models.ImageField(
        upload_to="site_messages/",
        blank=True,
        null=True,
        validators=[validate_image_size]
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "SiteMessage"
    
class BugReport(models.Model):
    REQUEST_TYPE_CHOICES = [
        ("bug", "Kvar"),
        ("question", "Pitanje"),
        ("idea", "Prijedlog"),
    ]

    TOPIC_CHOICES = [
        ("publishing", "Objavljivanje postova"),
        ("design", "Dizajn bloga"),
        ("profile", "Profil i račun"),
        ("comments", "Komentari i lajkovi"),
        ("boxes", "Boxevi i sidebar"),
        ("author", "Upoznaj autora"),
        ("other", "Ostalo"),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES, default="bug")
    topic = models.CharField(max_length=30, choices=TOPIC_CHOICES, default="other")
    title = models.CharField(max_length=200)
    description = models.TextField()
    email = models.EmailField(blank=True, default='')
    page_url = models.CharField(max_length=500, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_request_type_display()} - {self.title}"
    
class FeaturedPost(models.Model):
    KIND_CHOICES = (
        ("daily", "Dnevni"),
        ("weekly", "Tjedni"),
    )

    kind = models.CharField(max_length=10, choices=KIND_CHOICES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="featured_entries")
    period_start = models.DateTimeField()
    period_end = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["kind", "-period_start"]),
        ]

    def __str__(self):
        return f"{self.kind} - {self.post_id}"
    
class HomeFeaturedPost(models.Model):
    SOURCE_CHOICES = (
        ("algorithm", "Algoritam"),
        ("premium", "Premium"),
        ("admin", "Admin"),
    )

    SLOT_CHOICES = (
        ("morning", "Jutro"),
        ("afternoon", "Popodne"),
        ("evening", "Večer"),
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="home_featured_entries",
        null=True,
        blank=True,
    )
    source = models.CharField(max_length=12, choices=SOURCE_CHOICES, default="algorithm")
    featured_at = models.DateTimeField()
    slot_date = models.DateField(null=True, blank=True)
    slot_name = models.CharField(max_length=12, choices=SLOT_CHOICES, blank=True)
    slot_token = models.CharField(max_length=40, unique=True, null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    raw_score = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["source", "-featured_at"]),
            models.Index(fields=["slot_date", "slot_name"]),
        ]
        ordering = ["-featured_at", "-created_at"]

    def __str__(self):
        return f"{self.source} - {self.post_id or 'empty'} - {self.featured_at}"

class UserBlock(models.Model):
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blocking")
    blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blocked_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("blocker", "blocked")

    def __str__(self):
        return f"{self.blocker} blokira {self.blocked}"


class UserRestriction(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="restricted_users")
    restricted = models.ForeignKey(User, on_delete=models.CASCADE, related_name="restricted_by_users")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("owner", "restricted")

    def __str__(self):
        return f"{self.owner} ograničava {self.restricted}"



class BlogVisitor(models.Model):
    blog_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_visitors")
    visitor_token = models.CharField(max_length=64)
    page_label = models.CharField(max_length=50, blank=True, default="blog")
    path = models.CharField(max_length=255, blank=True, default="")
    device_type = models.CharField(max_length=20, blank=True, default="Nepoznato")
    user_agent = models.CharField(max_length=255, blank=True, default="")
    browser_language = models.CharField(max_length=32, blank=True, default="")
    timezone_name = models.CharField(max_length=64, blank=True, default="")
    country = models.CharField(max_length=80, blank=True, default="")
    country_code = models.CharField(max_length=8, blank=True, default="")
    city = models.CharField(max_length=80, blank=True, default="")
    latitude = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    longitude = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    hit_count = models.PositiveIntegerField(default=0)
    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["blog_owner", "visitor_token"], name="unique_blog_visitor_token"),
        ]
        indexes = [
            models.Index(fields=["blog_owner", "last_seen"]),
            models.Index(fields=["blog_owner", "page_label"]),
        ]

    def __str__(self):
        return f"{self.blog_owner.username} - {self.visitor_token[:8]}"

from datetime import date, timedelta


class SpecialDayEvent(models.Model):
    DATE_TYPE_CHOICES = (
        ("fixed", "Fiksni datum"),
        ("range", "Raspon datuma"),
        ("nth_weekday", "N-ti dan u mjesecu"),
        ("easter", "Uskrs"),
        ("advent", "Advent"),
        ("advent_sunday", "Došašće (1.–4. nedjelja)"),
    )

    POSITION_CHOICES = (
        ("top", "Iznad postova"),
        ("left", "Iznad lijevog sidebara"),
        ("right", "Iznad desnog sidebara"),
    )

    THEME_CHOICES = (
        ("general", "Općenito"),
        ("romance", "Valentinovo / romantika"),
        ("womens_day", "Dan žena"),
        ("spring", "Proljeće"),
        ("earth", "Dan planeta Zemlje"),
        ("books", "Dan knjige"),
        ("summer", "Ljeto"),
        ("autumn", "Jesen"),
        ("bread", "Dani kruha"),
        ("advent", "Advent"),
        ("advent_candle_1", "Došašće – 1. svijeća"),
        ("advent_candle_2", "Došašće – 2. svijeća"),
        ("advent_candle_3", "Došašće – 3. svijeća"),
        ("advent_candle_4", "Došašće – 4. svijeća"),
        ("christmas", "Božić"),
        ("easter", "Uskrs"),
        ("new_year", "Nova godina"),
        ("old_year", "Stara godina"),
    )

    WEEKDAY_CHOICES = (
        (0, "Ponedjeljak"),
        (1, "Utorak"),
        (2, "Srijeda"),
        (3, "Četvrtak"),
        (4, "Petak"),
        (5, "Subota"),
        (6, "Nedjelja"),
    )

    WEEK_ORDER_CHOICES = (
        (1, "Prvi"),
        (2, "Drugi"),
        (3, "Treći"),
        (4, "Četvrti"),
        (5, "Zadnji"),
    )

    name = models.CharField(max_length=120)
    is_active = models.BooleanField(default=True)
    priority = models.PositiveIntegerField(default=100)
    position = models.CharField(max_length=10, choices=POSITION_CHOICES, default="top")
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default="general")
    date_type = models.CharField(max_length=20, choices=DATE_TYPE_CHOICES, default="fixed")

    month = models.PositiveSmallIntegerField(blank=True, null=True)
    day = models.PositiveSmallIntegerField(blank=True, null=True)

    start_month = models.PositiveSmallIntegerField(blank=True, null=True)
    start_day = models.PositiveSmallIntegerField(blank=True, null=True)
    end_month = models.PositiveSmallIntegerField(blank=True, null=True)
    end_day = models.PositiveSmallIntegerField(blank=True, null=True)

    nth_month = models.PositiveSmallIntegerField(blank=True, null=True)
    nth_week = models.PositiveSmallIntegerField(blank=True, null=True, choices=WEEK_ORDER_CHOICES)
    nth_weekday = models.PositiveSmallIntegerField(blank=True, null=True, choices=WEEKDAY_CHOICES)

    accent_label = models.CharField(max_length=80, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["priority", "id"]

    def __str__(self):
        return self.name

    @staticmethod
    def get_easter_sunday(year):
        a = year % 19
        b = year // 100
        c = year % 100
        d = b // 4
        e = b % 4
        f = (b + 8) // 25
        g = (b - f + 1) // 3
        h = (19 * a + b - d - g + 15) % 30
        i = c // 4
        k = c % 4
        l = (32 + 2 * e + 2 * i - h - k) % 7
        m = (a + 11 * h + 22 * l) // 451
        month = (h + l - 7 * m + 114) // 31
        day = ((h + l - 7 * m + 114) % 31) + 1
        return date(year, month, day)

    @staticmethod
    def get_advent_start(year):
        christmas = date(year, 12, 25)
        weekday = christmas.weekday()
        previous_sunday = christmas - timedelta(days=(weekday + 1) % 7)
        return previous_sunday - timedelta(weeks=3)

    @staticmethod
    def _build_month_day(year, month, day):
        return date(year, month, day)

    def matches_date(self, check_date):
        if not self.is_active:
            return False

        if self.date_type == "fixed":
            return self.month == check_date.month and self.day == check_date.day

        if self.date_type == "range":
            if not all([self.start_month, self.start_day, self.end_month, self.end_day]):
                return False
            start = self._build_month_day(check_date.year, self.start_month, self.start_day)
            end = self._build_month_day(check_date.year, self.end_month, self.end_day)
            current = check_date
            if end >= start:
                return start <= current <= end
            return current >= start or current <= end

        if self.date_type == "nth_weekday":
            if self.nth_month != check_date.month or self.nth_weekday is None or self.nth_week is None:
                return False
            matching_days = []
            day_cursor = date(check_date.year, check_date.month, 1)
            while day_cursor.month == check_date.month:
                if day_cursor.weekday() == self.nth_weekday:
                    matching_days.append(day_cursor.day)
                day_cursor += timedelta(days=1)
            if not matching_days:
                return False
            target_day = matching_days[-1] if self.nth_week == 5 else matching_days[self.nth_week - 1] if len(matching_days) >= self.nth_week else None
            return target_day == check_date.day

        if self.date_type == "easter":
            return self.get_easter_sunday(check_date.year) == check_date

        if self.date_type == "advent":
            start = self.get_advent_start(check_date.year)
            end = date(check_date.year, 12, 24)
            return start <= check_date <= end

        if self.date_type == "advent_sunday":
            if not self.nth_week or self.nth_week not in (1, 2, 3, 4):
                return False
            start = self.get_advent_start(check_date.year)
            target = start + timedelta(weeks=self.nth_week - 1)
            return target == check_date

        return False


class SpecialDayMessage(models.Model):
    event = models.ForeignKey(SpecialDayEvent, on_delete=models.CASCADE, related_name="messages")
    title = models.CharField(max_length=160, blank=True, default="")
    body = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title or f"Poruka za {self.event.name}"


class SpecialDaySelection(models.Model):
    event = models.ForeignKey(SpecialDayEvent, on_delete=models.CASCADE, related_name="selections")
    message = models.ForeignKey(SpecialDayMessage, on_delete=models.CASCADE, related_name="selections")
    selection_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("event", "selection_date")
        ordering = ["-selection_date", "-id"]

    def __str__(self):
        return f"{self.event.name} - {self.selection_date}"

class SecurityEvent(models.Model):
    EVENT_TYPE_CHOICES = (
        ("login_success", "Uspješna prijava"),
        ("login_failed", "Neuspješna prijava"),
        ("login_lockout", "Blokirana prijava"),
        ("registration_success", "Uspješna registracija"),
        ("registration_blocked", "Blokirana registracija"),
        ("turnstile_failed", "Turnstile nije prošao"),
        ("activation_success", "Račun aktiviran"),
        ("activation_failed", "Neuspješna aktivacija"),
        ("resend_email_success", "Ponovno poslan email"),
        ("resend_email_blocked", "Blokirano ponovno slanje emaila"),
        ("password_change_success", "Lozinka promijenjena"),
        ("password_change_failed", "Neuspješna promjena lozinke"),
        ("email_change_requested", "Zatražena promjena emaila"),
        ("email_change_confirmed", "Email potvrđen"),
        ("comment_rate_limited", "Komentiranje ograničeno"),
        ("duplicate_comment_blocked", "Dupli komentar blokiran"),
        ("post_deleted", "Post izbrisan"),
        ("avatar_deleted", "Avatar izbrisan"),
        ("suspicious_access", "Sumnjiv pristup"),
    )

    SEVERITY_CHOICES = (
        ("info", "Info"),
        ("warning", "Upozorenje"),
        ("critical", "Kritično"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="security_events",
    )
    username = models.CharField(max_length=150, blank=True, default="")
    event_type = models.CharField(max_length=60, choices=EVENT_TYPE_CHOICES)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default="info")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True, default="")
    path = models.CharField(max_length=255, blank=True, default="")
    method = models.CharField(max_length=10, blank=True, default="")
    message = models.TextField(blank=True, default="")
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["event_type", "created_at"]),
            models.Index(fields=["severity", "created_at"]),
            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["ip_address", "created_at"]),
        ]

    def __str__(self):
        who = self.username or (self.user.username if self.user else "anonimno")
        return f"{self.get_event_type_display()} - {who} - {self.created_at:%d.%m.%Y %H:%M}"

# ==========================================================
# POZADINSKA GLAZBA ZA BLOGOVE
# ==========================================================

def validate_audio_size(audio):
    from django.conf import settings

    max_mb = int(getattr(settings, "MAX_AUDIO_UPLOAD_SIZE_MB", 20))
    max_size = max_mb * 1024 * 1024

    if audio.size > max_size:
        raise ValidationError(f"Audio datoteka je prevelika (max {max_mb}MB).")


def validate_audio_extension(audio):
    allowed_extensions = [".mp3", ".ogg", ".wav", ".m4a"]
    name = (audio.name or "").lower()

    if not any(name.endswith(ext) for ext in allowed_extensions):
        raise ValidationError("Dopušteni audio formati su: MP3, OGG, WAV i M4A.")


class AmbientMusicTrack(models.Model):
    CATEGORY_CHOICES = [
        ("calm", "Mirno i opuštajuće"),
        ("romantic", "Nježno i romantično"),
        ("jazz", "Jazz i lounge"),
        ("fantasy", "Čarobno i fantasy"),
        ("mystery", "Tajanstveno i napeto"),
        ("cinematic", "Putovanje i filmski ugođaj"),
        ("fun", "Veselo i posebno"),
        ("other", "Ostalo"),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default="other"
    )
    description = models.CharField(max_length=300, blank=True)
    artist = models.CharField(max_length=120, blank=True, default="BlogPlatform")

    audio_file = models.FileField(
        upload_to="ambient_music/",
        validators=[validate_audio_size, validate_audio_extension]
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Pozadinska glazba"
        verbose_name_plural = "Pozadinska glazba"
        ordering = ["category", "title"]

    def __str__(self):
        return self.title

