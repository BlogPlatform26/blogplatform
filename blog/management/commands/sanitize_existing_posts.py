from django.core.management.base import BaseCommand

from blog.html_sanitizer import sanitize_post_html
from blog.models import Post


class Command(BaseCommand):
    help = "Sanitizira postojeći CKEditor HTML sadržaj u postovima."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Samo prikaži koliko bi postova bilo promijenjeno, bez spremanja.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        changed_count = 0

        for post in Post.objects.all().only("id", "title", "content"):
            old_content = post.content or ""
            new_content = sanitize_post_html(old_content)

            if new_content != old_content:
                changed_count += 1

                if not dry_run:
                    post.content = new_content
                    post.save(update_fields=["content"])

        if dry_run:
            self.stdout.write(self.style.WARNING(
                f"Dry run: {changed_count} postova bi bilo očišćeno."
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f"Gotovo: očišćeno je {changed_count} postova."
            ))
