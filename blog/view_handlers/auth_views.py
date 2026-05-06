import hashlib
import json
import time
import urllib.error
import urllib.parse
import urllib.request

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives, send_mail
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.http import require_POST

from blog.forms import AuthorProfileForm, CustomUserCreationForm, ProfileUpdateForm, UserUpdateForm
from blog.services import set_blog_preferences
from blog.security import log_security_event


PENDING_ACTIVATION_SESSION_KEY = 'pending_activation_user_id'



def _get_client_ip(request):
    """
    Vrati IP adresu korisnika.
    Ako je aplikacija iza proxyja, uzima prvi IP iz X-Forwarded-For.
    """
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', 'unknown')



def _login_rate_cache_keys(request, username):
    """
    Cache key ne smije imati čudne znakove, zato koristimo SHA256 hash.
    Zaključavanje ide po kombinaciji IP adrese i korisničkog imena.
    """
    ip_address = _get_client_ip(request)
    normalized_username = (username or '').strip().lower() or 'empty'
    raw_key = f'{ip_address}:{normalized_username}'
    key_hash = hashlib.sha256(raw_key.encode('utf-8')).hexdigest()

    return {
        'attempts': f'login_attempts:{key_hash}',
        'lock': f'login_lock:{key_hash}',
    }



def _get_login_lock_seconds_left(request, username):
    keys = _login_rate_cache_keys(request, username)
    lock_until = cache.get(keys['lock'])

    if not lock_until:
        return 0

    now = int(time.time())

    try:
        lock_until = int(lock_until)
    except (TypeError, ValueError):
        cache.delete(keys['lock'])
        return 0

    seconds_left = lock_until - now

    if seconds_left <= 0:
        cache.delete(keys['lock'])
        cache.delete(keys['attempts'])
        return 0

    return seconds_left



def _register_failed_login_attempt(request, username):
    keys = _login_rate_cache_keys(request, username)

    max_attempts = getattr(settings, 'LOGIN_MAX_ATTEMPTS', 5)
    window_seconds = getattr(settings, 'LOGIN_RATE_LIMIT_WINDOW_SECONDS', 600)
    lockout_seconds = getattr(settings, 'LOGIN_LOCKOUT_SECONDS', 600)

    try:
        attempts = int(cache.get(keys['attempts']) or 0)
    except (TypeError, ValueError):
        attempts = 0

    attempts += 1
    cache.set(keys['attempts'], attempts, timeout=window_seconds)

    if attempts >= max_attempts:
        lock_until = int(time.time()) + lockout_seconds
        cache.set(keys['lock'], lock_until, timeout=lockout_seconds)
        return attempts, 0, lockout_seconds

    remaining = max(max_attempts - attempts, 0)
    return attempts, remaining, 0



def _clear_failed_login_attempts(request, username):
    keys = _login_rate_cache_keys(request, username)
    cache.delete(keys['attempts'])
    cache.delete(keys['lock'])


def _registration_rate_cache_keys(request):
    """
    Ograničenje registracije ide po IP adresi.
    Ovo sprječava brzo masovno otvaranje računa s iste adrese.
    """
    ip_address = _get_client_ip(request)
    key_hash = hashlib.sha256(ip_address.encode('utf-8')).hexdigest()

    return {
        'attempts': f'registration_attempts:{key_hash}',
        'lock': f'registration_lock:{key_hash}',
    }



def _get_registration_lock_seconds_left(request):
    keys = _registration_rate_cache_keys(request)
    lock_until = cache.get(keys['lock'])

    if not lock_until:
        return 0

    now = int(time.time())

    try:
        lock_until = int(lock_until)
    except (TypeError, ValueError):
        cache.delete(keys['lock'])
        return 0

    seconds_left = lock_until - now

    if seconds_left <= 0:
        cache.delete(keys['lock'])
        cache.delete(keys['attempts'])
        return 0

    return seconds_left


def _register_registration_attempt(request):
    keys = _registration_rate_cache_keys(request)

    max_attempts = getattr(settings, 'REGISTRATION_MAX_ATTEMPTS', 5)
    window_seconds = getattr(settings, 'REGISTRATION_RATE_LIMIT_WINDOW_SECONDS', 3600)
    lockout_seconds = getattr(settings, 'REGISTRATION_LOCKOUT_SECONDS', 3600)

    try:
        attempts = int(cache.get(keys['attempts']) or 0)
    except (TypeError, ValueError):
        attempts = 0

    attempts += 1
    cache.set(keys['attempts'], attempts, timeout=window_seconds)

    if attempts > max_attempts:
        lock_until = int(time.time()) + lockout_seconds
        cache.set(keys['lock'], lock_until, timeout=lockout_seconds)
        return attempts, 0, lockout_seconds

    remaining = max(max_attempts - attempts, 0)
    return attempts, remaining, 0


def _resend_email_rate_cache_keys(request, user, purpose):
    """
    Ograničenje ponovnog slanja emaila ide po korisniku, IP adresi i svrsi.
    Svrha može biti npr. "activation" ili "email_change".
    """
    ip_address = _get_client_ip(request)
    user_id = getattr(user, 'id', None) or 'unknown'
    raw_key = f'{purpose}:{user_id}:{ip_address}'
    key_hash = hashlib.sha256(raw_key.encode('utf-8')).hexdigest()

    return {
        'attempts': f'resend_email_attempts:{key_hash}',
        'lock': f'resend_email_lock:{key_hash}',
    }



def _get_resend_email_lock_seconds_left(request, user, purpose):
    keys = _resend_email_rate_cache_keys(request, user, purpose)
    lock_until = cache.get(keys['lock'])

    if not lock_until:
        return 0

    now = int(time.time())

    try:
        lock_until = int(lock_until)
    except (TypeError, ValueError):
        cache.delete(keys['lock'])
        return 0

    seconds_left = lock_until - now

    if seconds_left <= 0:
        cache.delete(keys['lock'])
        cache.delete(keys['attempts'])
        return 0

    return seconds_left



def _register_resend_email_attempt(request, user, purpose):
    keys = _resend_email_rate_cache_keys(request, user, purpose)

    max_attempts = getattr(settings, 'RESEND_EMAIL_MAX_ATTEMPTS', 3)
    window_seconds = getattr(settings, 'RESEND_EMAIL_RATE_LIMIT_WINDOW_SECONDS', 900)
    lockout_seconds = getattr(settings, 'RESEND_EMAIL_LOCKOUT_SECONDS', 900)

    try:
        attempts = int(cache.get(keys['attempts']) or 0)
    except (TypeError, ValueError):
        attempts = 0

    attempts += 1
    cache.set(keys['attempts'], attempts, timeout=window_seconds)

    if attempts > max_attempts:
        lock_until = int(time.time()) + lockout_seconds
        cache.set(keys['lock'], lock_until, timeout=lockout_seconds)
        return attempts, 0, lockout_seconds

    remaining = max(max_attempts - attempts, 0)
    return attempts, remaining, 0



def _can_resend_email(request, user, purpose):
    seconds_left = _get_resend_email_lock_seconds_left(request, user, purpose)
    if seconds_left > 0:
        return False, seconds_left

    attempts, remaining, lockout_seconds = _register_resend_email_attempt(request, user, purpose)
    if lockout_seconds > 0:
        return False, lockout_seconds

    return True, 0



def _format_seconds_as_minutes(seconds):
    minutes = max(1, int((seconds + 59) // 60))
    if minutes == 1:
        return '1 minutu'
    return f'{minutes} minuta'




def _register_context(form):
    return {
        'form': form,
        'turnstile_enabled': getattr(settings, 'TURNSTILE_ENABLED', False),
        'turnstile_site_key': getattr(settings, 'TURNSTILE_SITE_KEY', ''),
    }


def _verify_turnstile(request):
    """
    Provjerava Cloudflare Turnstile token na serveru.
    Ako TURNSTILE_ENABLED=False, provjera se preskače.
    """
    if not getattr(settings, 'TURNSTILE_ENABLED', False):
        return True, ''

    site_key = (getattr(settings, 'TURNSTILE_SITE_KEY', '') or '').strip()
    secret_key = (getattr(settings, 'TURNSTILE_SECRET_KEY', '') or '').strip()

    if not site_key or not secret_key:
        return False, 'Sigurnosna provjera nije pravilno podešena.'

    token = (request.POST.get('cf-turnstile-response') or '').strip()
    if not token:
        return False, 'Potvrdi sigurnosnu provjeru prije registracije.'

    payload = urllib.parse.urlencode({
        'secret': secret_key,
        'response': token,
        'remoteip': _get_client_ip(request),
    }).encode('utf-8')

    verify_request = urllib.request.Request(
        'https://challenges.cloudflare.com/turnstile/v0/siteverify',
        data=payload,
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        method='POST',
    )

    try:
        with urllib.request.urlopen(verify_request, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError):
        return False, 'Sigurnosna provjera trenutno nije dostupna. Pokušaj ponovno.'

    if result.get('success') is True:
        return True, ''

    return False, 'Sigurnosna provjera nije prošla. Pokušaj ponovno.'


def _store_pending_activation_user(request, user):
    request.session[PENDING_ACTIVATION_SESSION_KEY] = user.id
    request.session.modified = True



def _clear_pending_activation_user(request):
    request.session.pop(PENDING_ACTIVATION_SESSION_KEY, None)
    request.session.modified = True



def _get_pending_activation_user(request):
    user_id = request.session.get(PENDING_ACTIVATION_SESSION_KEY)
    if not user_id:
        return None
    return User.objects.filter(pk=user_id, is_active=False).first()



def _build_activation_url(request, user):
    site_url = (getattr(settings, 'SITE_URL', '') or '').strip().rstrip('/')
    if not site_url:
        current_site = get_current_site(request)
        site_url = f"http://{current_site.domain}".rstrip('/')

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return f"{site_url}/activate/{uid}/{token}/"



def _send_activation_email(request, user):
    activation_url = _build_activation_url(request, user)

    context = {
        'user': user,
        'activation_url': activation_url,
    }

    text_body = render_to_string('blog/activation_email.txt', context)
    html_body = render_to_string('blog/activation_email.html', context)

    email = EmailMultiAlternatives(
        subject='Aktivirajte svoj račun',
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.attach_alternative(html_body, 'text/html')

    sent_count = email.send(fail_silently=False)
    print(f'AKTIVACIJSKI MAIL POSLAN: {sent_count} -> {user.email}')
    return sent_count



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        seconds_left = _get_registration_lock_seconds_left(request)
        if seconds_left > 0:
            log_security_event(
                request,
                event_type='registration_blocked',
                severity='warning',
                message='Pokušaj registracije tijekom aktivne blokade.',
                metadata={'seconds_left': seconds_left},
            )
            messages.error(
                request,
                f'Previše pokušaja registracije. Pokušaj ponovno za {_format_seconds_as_minutes(seconds_left)}.'
            )
            return render(request, 'blog/register.html', _register_context(form))

        attempts, remaining, lockout_seconds = _register_registration_attempt(request)
        if lockout_seconds > 0:
            log_security_event(
                request,
                event_type='registration_blocked',
                severity='warning',
                message='Registracija blokirana zbog previše pokušaja.',
                metadata={'attempts': attempts, 'lockout_seconds': lockout_seconds},
            )
            messages.error(
                request,
                f'Previše pokušaja registracije. Pokušaj ponovno za {_format_seconds_as_minutes(lockout_seconds)}.'
            )
            return render(request, 'blog/register.html', _register_context(form))

        turnstile_ok, turnstile_error = _verify_turnstile(request)
        if not turnstile_ok:
            log_security_event(
                request,
                event_type='turnstile_failed',
                severity='warning',
                message='Turnstile provjera na registraciji nije prošla.',
                metadata={'error': turnstile_error},
            )
            form.add_error(None, turnstile_error)
            return render(request, 'blog/register.html', _register_context(form))

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            profile = user.profile
            profile.blog_name = form.cleaned_data['blog_name']
            profile.save()

            set_blog_preferences(user, {
                'cursor_style': 'default',
                'cursor_effect': 'none',
            })

            try:
                sent_count = _send_activation_email(request, user)
            except Exception as exc:
                user.delete()
                form.add_error(None, f'Mail za aktivaciju nije poslan: {exc}')
                return render(request, 'blog/register.html', _register_context(form))

            if sent_count != 1:
                user.delete()
                form.add_error(None, 'Mail za aktivaciju nije poslan. Pokušaj ponovno.')
                return render(request, 'blog/register.html', _register_context(form))

            _store_pending_activation_user(request, user)
            log_security_event(
                request,
                event_type='registration_success',
                user=user,
                severity='info',
                message='Novi korisnički račun je registriran i čeka aktivaciju.',
                metadata={'email': user.email},
            )
            return redirect('activation_sent')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', _register_context(form))


def activation_sent(request):
    pending_user = _get_pending_activation_user(request)
    if not pending_user:
        messages.info(request, 'Nema računa koji čeka aktivaciju.')
        return redirect('login')

    if request.method == 'POST':
        can_send, seconds_left = _can_resend_email(request, pending_user, 'activation')
        if not can_send:
            log_security_event(
                request,
                event_type='resend_email_blocked',
                user=pending_user,
                severity='warning',
                message='Blokirano ponovno slanje aktivacijskog emaila.',
                metadata={'purpose': 'activation', 'seconds_left': seconds_left},
            )
            messages.error(
                request,
                f'Previše zahtjeva za ponovno slanje emaila. Pokušaj ponovno za {_format_seconds_as_minutes(seconds_left)}.'
            )
            return redirect('activation_sent')

        try:
            sent_count = _send_activation_email(request, pending_user)
            if sent_count == 1:
                log_security_event(
                    request,
                    event_type='resend_email_success',
                    user=pending_user,
                    severity='info',
                    message='Aktivacijski email je ponovno poslan.',
                    metadata={'purpose': 'activation'},
                )
                messages.success(request, 'Aktivacijski mail je ponovno poslan.')
            else:
                messages.error(request, 'Mail nije ponovno poslan.')
        except Exception as exc:
            messages.error(request, f'Mail nije ponovno poslan: {exc}')
        return redirect('activation_sent')

    return render(request, 'blog/activation_sent.html', {
        'pending_user_email': pending_user.email,
        'pending_username': pending_user.username,
    })



def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        _clear_pending_activation_user(request)
        log_security_event(
            request,
            event_type='activation_success',
            user=user,
            severity='info',
            message='Račun je uspješno aktiviran.',
        )
        messages.success(request, 'Račun je uspješno aktiviran.')
        return redirect('author_onboarding')
    log_security_event(
        request,
        event_type='activation_failed',
        severity='warning',
        message='Neuspješna aktivacija računa.',
        metadata={'uidb64': uidb64},
    )
    return render(request, 'blog/activation_invalid.html')



def _get_user_by_login_identifier(identifier):
    """
    Korisnik se može prijaviti korisničkim imenom ili email adresom.
    Vraća korisnika ako postoji, inače None.
    """
    identifier = (identifier or '').strip()

    if not identifier:
        return None

    if '@' in identifier:
        user_by_email = User.objects.filter(email__iexact=identifier).first()
        if user_by_email:
            return user_by_email

    return User.objects.filter(username__iexact=identifier).first()


def custom_login(request):
    if request.method == 'POST':
        login_identifier = (request.POST.get('username') or '').strip()
        password = request.POST.get('password') or ''

        seconds_left = _get_login_lock_seconds_left(request, login_identifier)
        if seconds_left > 0:
            log_security_event(
                request,
                event_type='login_lockout',
                severity='warning',
                message='Pokušaj prijave tijekom aktivne blokade.',
                metadata={'login_identifier': login_identifier, 'seconds_left': seconds_left},
            )
            messages.error(
                request,
                f'Previše neuspješnih pokušaja prijave. Pokušaj ponovno za {_format_seconds_as_minutes(seconds_left)}.'
            )
            return render(request, 'blog/login.html')

        user_obj = _get_user_by_login_identifier(login_identifier)

        # Django authenticate prima username, zato kod email prijave prvo nađemo korisnika
        # pa autentikaciju radimo s njegovim stvarnim korisničkim imenom.
        auth_username = user_obj.username if user_obj else login_identifier
        user = authenticate(request, username=auth_username, password=password)

        if user is not None:
            _clear_failed_login_attempts(request, login_identifier)
            login(request, user)
            log_security_event(
                request,
                event_type='login_success',
                user=user,
                severity='info',
                message='Korisnik se uspješno prijavio.',
                metadata={'login_identifier': login_identifier},
            )
            return redirect('home')

        # Ovu poruku pokažemo samo ako su podaci točni, ali račun još nije aktiviran.
        # Ako je lozinka kriva, ispod ide općenita poruka.
        if user_obj and not user_obj.is_active and user_obj.check_password(password):
            _clear_failed_login_attempts(request, login_identifier)
            _store_pending_activation_user(request, user_obj)
            log_security_event(
                request,
                event_type='login_failed',
                user=user_obj,
                severity='warning',
                message='Pokušaj prijave na neaktiviran račun.',
                metadata={'login_identifier': login_identifier, 'reason': 'inactive_account'},
            )
            messages.error(request, 'Račun još nije aktiviran. Provjeri email ili pošalji aktivacijski mail ponovno.')
            return redirect('activation_sent')

        attempts, remaining, lockout_seconds = _register_failed_login_attempt(request, login_identifier)

        if lockout_seconds > 0:
            log_security_event(
                request,
                event_type='login_lockout',
                user=user_obj,
                severity='warning',
                message='Korisnik/IP je blokiran zbog previše neuspješnih prijava.',
                metadata={
                    'login_identifier': login_identifier,
                    'attempts': attempts,
                    'lockout_seconds': lockout_seconds,
                },
            )
            messages.error(
                request,
                f'Previše neuspješnih pokušaja prijave. Pokušaj ponovno za {_format_seconds_as_minutes(lockout_seconds)}.'
            )
        else:
            log_security_event(
                request,
                event_type='login_failed',
                user=user_obj,
                severity='warning',
                message='Neuspješna prijava.',
                metadata={
                    'login_identifier': login_identifier,
                    'attempts': attempts,
                    'remaining': remaining,
                    'user_exists': bool(user_obj),
                },
            )
            messages.error(
                request,
                f'Podaci za prijavu nisu ispravni. Preostalo pokušaja: {remaining}.'
            )

    return render(request, 'blog/login.html')


@login_required
def author_onboarding(request):
    profile = request.user.profile
    if request.method == 'POST':
        if 'skip_author_onboarding' in request.POST:
            messages.info(request, 'Dio O autoru možeš ispuniti kasnije u postavkama.')
            return redirect('profile')

        author_form = AuthorProfileForm(request.POST, instance=profile)
        if author_form.is_valid():
            saved_profile = author_form.save(commit=False)
            saved_profile.author_contact = profile.author_contact
            saved_profile.author_social_links = profile.author_social_links
            saved_profile.author_website = profile.author_website
            saved_profile.allow_author_questions = profile.allow_author_questions
            saved_profile.save()
            messages.success(request, 'Podaci o autoru su spremljeni.')
            return redirect('profile')
    else:
        author_form = AuthorProfileForm(instance=profile)

    return render(request, 'blog/author_onboarding.html', {
        'author_form': author_form,
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            old_email = User.objects.get(pk=request.user.pk).email
            new_email = user_form.cleaned_data['email']

            request.user.username = user_form.cleaned_data['username']
            request.user.save()

            profile = profile_form.save(commit=False)
            if old_email != new_email:
                profile.pending_email = new_email
                profile.save()

                current_site = get_current_site(request)
                message = render_to_string('blog/change_email_email.html', {
                    'user': request.user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
                    'token': default_token_generator.make_token(request.user),
                })
                EmailMultiAlternatives(
                    'Potvrdite promjenu email adrese',
                    message,
                    settings.EMAIL_HOST_USER,
                    [new_email],
                ).send()

                warning_message = (
                    f'Pozdrav {request.user.username},\n\n'
                    'Zatražena je promjena email adrese vašeg računa.\n\n'
                    f'Nova adresa: {new_email}\n\n'
                    'Ako ovo niste bili vi, odmah promijenite lozinku.\n'
                )
                EmailMultiAlternatives(
                    'Zatražena je promjena email adrese',
                    warning_message,
                    settings.EMAIL_HOST_USER,
                    [old_email],
                ).send()
                log_security_event(
                    request,
                    event_type='email_change_requested',
                    user=request.user,
                    severity='warning',
                    message='Korisnik je zatražio promjenu email adrese.',
                    metadata={'old_email': old_email, 'new_email': new_email},
                )
                messages.success(request, 'Poslan je email za potvrdu nove adrese.')
                return redirect('profile')

            profile.save()
            messages.success(request, 'Podaci su uspješno spremljeni.')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'blog/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })



def confirm_email_change(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        profile = user.profile
        if profile.pending_email:
            user.email = profile.pending_email
            profile.pending_email = None
            user.save()
            profile.save()
            log_security_event(
                request,
                event_type='email_change_confirmed',
                user=user,
                severity='info',
                message='Email adresa je uspješno potvrđena.',
                metadata={'email': user.email},
            )
            messages.success(request, 'Email adresa je uspješno potvrđena.')
        return redirect('profile')

    messages.error(request, 'Link nije valjan ili je istekao.')
    return redirect('profile')


@login_required
@require_POST
def resend_confirmation_email(request):
    user = request.user
    if not user.profile.pending_email:
        messages.warning(request, 'Nema email adrese za potvrdu.')
        return redirect('home')

    can_send, seconds_left = _can_resend_email(request, user, 'email_change')
    if not can_send:
        log_security_event(
            request,
            event_type='resend_email_blocked',
            user=user,
            severity='warning',
            message='Blokirano ponovno slanje emaila za potvrdu nove adrese.',
            metadata={'purpose': 'email_change', 'seconds_left': seconds_left},
        )
        messages.error(
            request,
            f'Previše zahtjeva za ponovno slanje emaila. Pokušaj ponovno za {_format_seconds_as_minutes(seconds_left)}.'
        )
        return redirect('home')

    current_site = get_current_site(request)
    confirmation_link = f"http://{current_site.domain}/confirm-email/{urlsafe_base64_encode(force_bytes(user.pk))}/{default_token_generator.make_token(user)}/"
    send_mail(
        subject='Potvrda email adrese',
        message=f'Kliknite na link za potvrdu: {confirmation_link}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.profile.pending_email],
        fail_silently=False,
    )
    log_security_event(
        request,
        event_type='resend_email_success',
        user=user,
        severity='info',
        message='Email za potvrdu nove email adrese je ponovno poslan.',
        metadata={'purpose': 'email_change'},
    )
    messages.success(request, 'Mail za potvrdu je ponovno poslan.')
    return redirect('home')
