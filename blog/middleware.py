
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
