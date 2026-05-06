from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver


def validate_image_size(image):
    if image.size > 2 * 1024 * 1024:
        raise ValidationError("Slika je prevelika (max 2MB).")


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
        ("deleted", "Obrisan"),
    ]

    # ✅ NOVO: tip posta
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

    # 🔥 Slika posta
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

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts"
    )

    # ✅ TAGOVI (više tagova po postu)
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="posts"
    )

    # 🔵 Slika koja se koristi samo za HOME (automatski dodijeljena)
    home_image = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    # ✅ NOVO: tip posta
    post_type = models.CharField(
        max_length=10,
        choices=POST_TYPE_CHOICES,
        default="post"
    )

    def is_liked_by(self, user):
        if user.is_authenticated:
            return self.likes.filter(user=user).exists()
        return False

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
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
    background_color = models.CharField(max_length=20, default="#ffffff")

    # 🔴 Novo polje – čeka potvrdu emaila
    pending_email = models.EmailField(blank=True, null=True)

    TEMPLATE_CHOICES = (
        ("default", "Default"),
        ("dark", "Dark stil"),
        ("classic", "Classic stil"),
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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class FeaturedPost(models.Model):
    KIND_CHOICES = (
        ("daily", "Dnevni"),
        ("weekly", "Tjedni"),
    )

    kind = models.CharField(max_length=10, choices=KIND_CHOICES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="featured_entries")
    period_start = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["kind", "-period_start"]),
        ]

    def __str__(self):
        return f"{self.kind} - {self.post_id}"
    
class UserBlock(models.Model):
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blocking")
    blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blocked_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("blocker", "blocked")

    def __str__(self):
        return f"{self.blocker} blokira {self.blocked}"

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
