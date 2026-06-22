
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from blog.models import AccountStatus


class Command(BaseCommand):
    help = "Trajno briše korisničke račune koji su zatražili brisanje i čekali dovoljno dugo."

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=30,
            help="Koliko dana mora proći od zahtjeva za brisanje. Zadano: 30.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Samo prikaži što bi se obrisalo, bez stvarnog brisanja.",
        )

    def handle(self, *args, **options):
        days = options["days"]
        dry_run = options["dry_run"]

        cutoff = timezone.now() - timedelta(days=days)

        states = (
            AccountStatus.objects
            .select_related("user")
            .filter(
                status=AccountStatus.STATUS_DELETE_REQUESTED,
                deletion_requested_at__lte=cutoff,
            )
        )

        count = states.count()

        if count == 0:
            self.stdout.write(self.style.SUCCESS("Nema računa za trajno brisanje."))
            return

        for state in states:
            user = state.user
            label = f"{user.username} <{user.email}>"

            if dry_run:
                self.stdout.write(f"[DRY RUN] Obrisan bi bio: {label}")
            else:
                self.stdout.write(f"Brišem račun: {label}")
                user.delete()

        if dry_run:
            self.stdout.write(self.style.WARNING(f"Dry run gotov. Broj računa: {count}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Trajno obrisano računa: {count}"))
