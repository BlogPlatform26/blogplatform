from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from blog.models import Profile, SecurityEvent


class Command(BaseCommand):
    help = "Anonimizira korisnike koji su ranije soft deleteani."

    def handle(self, *args, **options):
        now = timezone.now()

        profiles = (
            Profile.objects
            .select_related("user")
            .filter(
                is_deleted=True,
                anonymized_at__isnull=True,
                anonymize_after__lte=now,
            )
        )

        count = 0
        for profile in profiles:
            user = profile.user
            old_username = user.username
            suffix = f"deleted_{user.id}"

            user.username = suffix
            user.email = f"{suffix}@deleted.local"
            user.first_name = ""
            user.last_name = ""
            user.set_unusable_password()
            user.is_active = False
            user.save(update_fields=["username", "email", "first_name", "last_name", "password", "is_active"])

            profile.blog_name = "Obrisan korisnik"
            profile.blog_tagline = ""
            profile.pending_email = None
            profile.author_bio = ""
            profile.author_full_name = ""
            profile.author_nickname = ""
            profile.author_birth_date = None
            profile.author_birth_place = ""
            profile.author_education = ""
            profile.author_occupation = ""
            profile.author_languages = ""
            profile.author_religion = ""
            profile.author_nationality = ""
            profile.author_hobbies = ""
            profile.author_interests = ""
            profile.author_favorite_topics = ""
            profile.author_inspiration = ""
            profile.author_motto = ""
            profile.author_contact = ""
            profile.author_social_links = ""
            profile.author_website = ""
            profile.anonymized_at = now

            if profile.avatar:
                profile.avatar.delete(save=False)
                profile.avatar = None
            if profile.blog_banner:
                profile.blog_banner.delete(save=False)
                profile.blog_banner = None
            if profile.simple_background_image:
                profile.simple_background_image.delete(save=False)
                profile.simple_background_image = None
            if profile.soho_hero_image:
                profile.soho_hero_image.delete(save=False)
                profile.soho_hero_image = None

            profile.save()

            try:
                SecurityEvent.objects.create(
                    user=None,
                    username=old_username,
                    event_type="account_anonymized",
                    severity="warning",
                    message="Soft delete korisnik je anonimiziran.",
                    metadata={"old_username": old_username, "new_username": suffix},
                )
            except Exception:
                pass

            count += 1

        self.stdout.write(self.style.SUCCESS(f"Anonimizirano korisnika: {count}"))
