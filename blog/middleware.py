
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect

from blog.models import AccountStatus


class AccountStatusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)

        if user is not None and user.is_authenticated:
            state = AccountStatus.objects.filter(user=user).first()

            if state and state.status in {
                AccountStatus.STATUS_DEACTIVATED,
                AccountStatus.STATUS_DELETE_REQUESTED,
            }:
                logout(request)

                if state.status == AccountStatus.STATUS_DELETE_REQUESTED:
                    messages.warning(
                        request,
                        "Tvoj račun je u postupku brisanja. Prijavi se ponovno kako bismo ti poslali email za otkazivanje brisanja."
                    )
                else:
                    messages.warning(
                        request,
                        "Tvoj račun je deaktiviran. Prijavi se ponovno kako bismo ti poslali email za aktivaciju."
                    )

                return redirect("login")

        return self.get_response(request)

# BLOGPLATFORM_AUTO_RANKINGS_START
class RankingAutoUpdateMiddleware:
    """
    Automatski pokreće update_rankings jednom dnevno.

    Ne treba ručno pokretati:
    python manage.py update_rankings

    Kada netko prvi put taj dan otvori stranicu, sustav provjeri cache
    i pokrene izračun za Post dana i Post tjedna.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self._maybe_update_rankings(request)
        return self.get_response(request)

    def _maybe_update_rankings(self, request):
        try:
            if request.method != "GET":
                return

            path = request.path or ""

            # Ne pokreći za statiku, media fileove i admin.
            if path.startswith("/static/") or path.startswith("/media/") or path.startswith("/admin/"):
                return

            from django.core.cache import cache
            from django.core.management import call_command
            from django.utils import timezone

            today = timezone.localdate().isoformat()

            done_key = f"blogplatform_rankings_updated_{today}"
            lock_key = f"blogplatform_rankings_update_lock_{today}"
            error_key = f"blogplatform_rankings_update_error_{today}"

            # Ako je danas već odrađeno, ne radi ništa.
            if cache.get(done_key):
                return

            # Ako je danas već pala greška, ne pokušavaj na svakom requestu.
            if cache.get(error_key):
                return

            # Zaključavanje da se ne pokrene više puta istovremeno.
            if not cache.add(lock_key, "1", timeout=300):
                return

            try:
                call_command("update_rankings", verbosity=0)

                # Pamti da je danas odrađeno.
                cache.set(done_key, "1", timeout=60 * 60 * 26)

            except Exception:
                # Ako nešto pukne, ne ruši stranicu.
                # Pokušat će opet kasnije.
                cache.set(error_key, "1", timeout=60 * 60)

            finally:
                cache.delete(lock_key)

        except Exception:
            # Ranking nikad ne smije srušiti stranicu.
            return
# BLOGPLATFORM_AUTO_RANKINGS_END
