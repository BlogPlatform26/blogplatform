from datetime import timedelta

from django.contrib import admin, messages
from django.utils import timezone

from .models import (
    AmbientMusicTrack,
    BugReport,
    Category,
    CategoryHomeImage,
    Comment,
    FeaturedPost,
    Follow,
    Like,
    Notification,
    PollOption,
    PollVote,
    Post,
    PostImage,
    Profile,
    QuizAnswer,
    QuizOption,
    SecurityEvent,
    SiteMessage,
    SpecialDayEvent,
    SpecialDayMessage,
    SpecialDaySelection,
    Tag,
    UserBlock,
    UserBox,
)


class CategoryHomeImageInline(admin.TabularInline):
    model = CategoryHomeImage
    extra = 1
    fields = ("title", "image", "is_active", "created_at")
    readonly_fields = ("created_at",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "group", "slug", "active_home_images_count")
    list_filter = ("group",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [CategoryHomeImageInline]

    @admin.display(description="Aktivne slike")
    def active_home_images_count(self, obj):
        return obj.home_images.filter(is_active=True).count()


class CategoryHomeImageAdmin(admin.ModelAdmin):
    list_display = ("category", "title", "is_active", "created_at")
    list_filter = ("category__group", "category", "is_active")
    search_fields = ("title", "category__name", "category__slug")
    readonly_fields = ("created_at",)


class SpecialDayMessageInline(admin.TabularInline):
    model = SpecialDayMessage
    extra = 1


@admin.register(SpecialDayEvent)
class SpecialDayEventAdmin(admin.ModelAdmin):
    list_display = ("name", "date_type", "position", "theme", "priority", "is_active")
    list_filter = ("date_type", "position", "theme", "is_active")
    search_fields = ("name", "accent_label")
    inlines = [SpecialDayMessageInline]


@admin.register(SpecialDayMessage)
class SpecialDayMessageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "event", "is_active", "order")
    list_filter = ("event", "is_active")
    search_fields = ("title", "body", "event__name")


@admin.register(SpecialDaySelection)
class SpecialDaySelectionAdmin(admin.ModelAdmin):
    list_display = ("event", "message", "selection_date", "created_at")
    list_filter = ("event", "selection_date")
    date_hierarchy = "selection_date"


@admin.register(BugReport)
class BugReportAdmin(admin.ModelAdmin):
    list_display = ("clean_title", "request_kind", "user", "is_resolved", "created_at")
    list_filter = ("is_resolved", "created_at")
    search_fields = ("title", "description", "user__username")

    def request_kind(self, obj):
        title = obj.title or ""
        if title.startswith("[PITANJE]"):
            return "Pitanje"
        if title.startswith("[PRIJEDLOG]"):
            return "Prijedlog"
        if title.startswith("[KVAR]"):
            return "Kvar"
        return "-"

    request_kind.short_description = "Vrsta"

    def clean_title(self, obj):
        title = obj.title or ""
        for prefix in ("[KVAR] ", "[PITANJE] ", "[PRIJEDLOG] "):
            if title.startswith(prefix):
                return title[len(prefix):]
        return title

    clean_title.short_description = "Naslov"




@admin.register(SecurityEvent)
class SecurityEventAdmin(admin.ModelAdmin):
    list_display = ("created_at", "event_type", "severity", "username", "user", "ip_address", "short_message")
    list_filter = ("event_type", "severity", "created_at")
    search_fields = ("username", "user__username", "ip_address", "message", "path", "user_agent")
    readonly_fields = (
        "created_at",
        "event_type",
        "severity",
        "user",
        "username",
        "ip_address",
        "user_agent",
        "path",
        "method",
        "message",
        "metadata",
    )
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    @admin.display(description="Poruka")
    def short_message(self, obj):
        return (obj.message or "")[:90]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "blog_name",
        "premium_access_active",
        "premium_mode",
        "premium_until",
        "template",
    )
    list_filter = ("template",)
    search_fields = ("user__username", "blog_name")
    actions = (
        "grant_temporary_premium_3_days",
        "grant_temporary_premium_7_days",
        "grant_temporary_premium_30_days",
        "clear_temporary_premium",
        "enable_permanent_premium",
        "disable_all_premium",
    )

    @admin.display(boolean=True, description="Premium aktivan")
    def premium_access_active(self, obj):
        return obj.has_active_premium

    @admin.display(description="Vrsta premiuma")
    def premium_mode(self, obj):
        return obj.premium_status_label

    @admin.action(description="Daj privremeni premium (3 dana)")
    def grant_temporary_premium_3_days(self, request, queryset):
        self._grant_temporary_premium(request, queryset, days=3)

    @admin.action(description="Daj privremeni premium (7 dana)")
    def grant_temporary_premium_7_days(self, request, queryset):
        self._grant_temporary_premium(request, queryset, days=7)

    @admin.action(description="Daj privremeni premium (30 dana)")
    def grant_temporary_premium_30_days(self, request, queryset):
        self._grant_temporary_premium(request, queryset, days=30)

    def _grant_temporary_premium(self, request, queryset, days):
        now = timezone.now()
        count = 0

        for profile in queryset:
            start_from = profile.premium_until if profile.premium_until and profile.premium_until > now else now
            profile.premium_until = start_from + timedelta(days=days)
            profile.save(update_fields=["premium_until"])
            count += 1

        self.message_user(
            request,
            f"Privremeni premium postavljen za {count} profila ({days} dana).",
            level=messages.SUCCESS,
        )

    @admin.action(description="Makni privremeni premium")
    def clear_temporary_premium(self, request, queryset):
        updated = queryset.exclude(premium_until__isnull=True).update(premium_until=None)
        self.message_user(
            request,
            f"Privremeni premium uklonjen za {updated} profila.",
            level=messages.SUCCESS,
        )

    @admin.action(description="Uključi trajni premium")
    def enable_permanent_premium(self, request, queryset):
        updated = queryset.update(is_premium=True)
        self.message_user(
            request,
            f"Trajni premium uključen za {updated} profila.",
            level=messages.SUCCESS,
        )

    @admin.action(description="Makni sav premium")
    def disable_all_premium(self, request, queryset):
        updated = queryset.update(is_premium=False, premium_until=None)
        self.message_user(
            request,
            f"Sav premium uklonjen za {updated} profila.",
            level=messages.SUCCESS,
        )


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CategoryHomeImage, CategoryHomeImageAdmin)
admin.site.register(Tag)
admin.site.register(UserBox)
admin.site.register(Follow)
admin.site.register(Notification)
admin.site.register(QuizOption)
admin.site.register(QuizAnswer)
admin.site.register(PollOption)
admin.site.register(PollVote)
admin.site.register(PostImage)
admin.site.register(Like)
admin.site.register(SiteMessage)
admin.site.register(FeaturedPost)
admin.site.register(UserBlock)


# ==========================================================
# UREDNIJI DJANGO ADMIN - GRUPIRANJE MODELA NA POČETNOJ STRANICI
# ==========================================================
# Ovo ne mijenja modele ni bazu. Samo mijenja raspored na /admin/
# da ne bude sve pod jednom velikom grupom "BLOG".

_ORIGINAL_GET_APP_LIST = admin.site.get_app_list


@admin.register(AmbientMusicTrack)
class AmbientMusicTrackAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "artist", "is_active", "created_at")
    list_filter = ("category", "is_active")
    search_fields = ("title", "artist", "description")
    readonly_fields = ("created_at",)

ADMIN_MODEL_GROUPS = [
    {
        "id": "security_moderation",
        "name": "Sigurnost i moderacija",
        "models": [
            "SecurityEvent",
            "UserRestriction",
            "UserBlock",
            "BugReport",
        ],
        "extra_security_overview": True,
    },
    {
        "id": "users_profiles",
        "name": "Korisnici i profili",
        "models": [
            "User",
            "Group",
            "Profile",
            "UserBox",
        ],
    },
    {
        "id": "posts_content",
        "name": "Postovi i sadržaj",
        "models": [
            "Post",
            "PostImage",
            "FeaturedPost",
            "HomeFeaturedPost",
            "Category",
            "CategoryHomeImage",
            "Tag",
        ],
    },
    {
        "id": "interactions_notifications",
        "name": "Interakcije i obavijesti",
        "models": [
            "Comment",
            "Like",
            "Follow",
            "Notification",
            "AuthorQuestion",
        ],
    },
    {
        "id": "quiz_poll",
        "name": "Kvizovi i ankete",
        "models": [
            "QuizOption",
            "QuizAnswer",
            "PollOption",
            "PollVote",
        ],
    },
    {
        "id": "platform_messages",
        "name": "Platforma i posebni dani",
        "models": [
            "SiteMessage",
            "SpecialDayEvent",
            "SpecialDayMessage",
            "SpecialDaySelection",
        ],
    },
    {
        "id": "design_multimedia",
        "name": "Dizajn i multimedija",
        "models": [
            "AmbientMusicTrack",
        ],
    },
    {
        "id": "analytics",
        "name": "Analitika",
        "models": [
            "BlogVisitor",
        ],
    },
]


def _security_overview_admin_row():
    return {
        "name": "Pregled sumnjivih aktivnosti",
        "object_name": "SecurityOverview",
        "perms": {"add": False, "change": False, "delete": False, "view": True},
        "admin_url": "/admin/security-events/overview/",
        "add_url": None,
        "view_only": True,
    }


def grouped_admin_app_list(request, app_label=None):
    """
    Django admin po defaultu grupira po app_labelu, zato svi blog modeli završe pod "BLOG".
    Ovdje samo presložimo prikaz početne admin stranice u praktičnije skupine.
    """
    if app_label:
        return _ORIGINAL_GET_APP_LIST(request, app_label)

    original_app_list = _ORIGINAL_GET_APP_LIST(request)

    all_models = []
    for app in original_app_list:
        for model in app.get("models", []):
            all_models.append(model)

    models_by_object_name = {
        model.get("object_name"): model
        for model in all_models
        if model.get("object_name")
    }

    used_object_names = set()
    grouped_app_list = []

    for group in ADMIN_MODEL_GROUPS:
        group_models = []

        if group.get("extra_security_overview"):
            group_models.append(_security_overview_admin_row())

        for object_name in group["models"]:
            model = models_by_object_name.get(object_name)
            if model and object_name not in used_object_names:
                group_models.append(model)
                used_object_names.add(object_name)

        # Ako grupa nema nijedan stvarni model i nema link na pregled, nemoj je prikazati.
        has_real_model = any(m.get("object_name") != "SecurityOverview" for m in group_models)
        has_overview = any(m.get("object_name") == "SecurityOverview" for m in group_models)
        if not has_real_model and not has_overview:
            continue

        grouped_app_list.append({
            "name": group["name"],
            "app_label": group["id"],
            "app_url": "",
            "has_module_perms": True,
            "models": group_models,
        })

    remaining_models = []
    for model in all_models:
        object_name = model.get("object_name")
        if object_name and object_name not in used_object_names:
            remaining_models.append(model)
            used_object_names.add(object_name)

    if remaining_models:
        grouped_app_list.append({
            "name": "Ostalo",
            "app_label": "other",
            "app_url": "",
            "has_module_perms": True,
            "models": remaining_models,
        })

    return grouped_app_list


admin.site.get_app_list = grouped_admin_app_list
admin.site.site_header = "BlogPlatform administracija"
admin.site.site_title = "BlogPlatform admin"
admin.site.index_title = "Administracija platforme"
