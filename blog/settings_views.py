import base64
import json
import os

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from PIL import Image, UnidentifiedImageError

from blog.forms import PostForm, UserBoxForm
from blog.models import (
    Category,
    PollOption,
    Post,
    PostImage,
    Profile,
    QuizOption,
    SiteMessage,
    UserBlock,
    UserBox,
    UserRestriction,
)
from blog.services import (
    apply_blog_preferences_to_profile,
    apply_tags_to_post,
    assign_home_image,
    get_allow_anonymous_comments,
    get_blog_preferences,
    get_design_font_choices,
    normalize_design_customizations,
    publish_due_posts,
    set_allow_anonymous_comments,
    set_blog_preferences,
)


MAX_BLOG_BANNER_SIZE = 2 * 1024 * 1024
MAX_BLOG_BANNER_WIDTH = 2200
MAX_BLOG_BANNER_HEIGHT = 900
MAX_BOXES_PER_SIDE = 3


DESIGN_TEMPLATE_META = {
    'default': {
        'label': 'Default',
        'description': 'Svijetli izgled',
        'preview_image': 'blog/images/design-previews/default.png',
    },
    'dark': {
        'label': 'Dark',
        'description': 'Tamni izgled',
        'preview_image': 'blog/images/design-previews/dark.png',
    },
    'classic': {
        'label': 'Classic',
        'description': 'Klasični izgled',
        'preview_image': 'blog/images/design-previews/classic.png',
    },
    'default_right': {
        'label': 'Default Plus',
        'description': 'Širi post i bočni stupci',
        'preview_image': 'blog/images/design-previews/default_right.png',
    },
    'dark_right': {
        'label': 'Dark Plus',
        'description': 'Širi post i bočni stupci',
        'preview_image': 'blog/images/design-previews/dark_right.png',
    },
    'classic_right': {
        'label': 'Classic Plus',
        'description': 'Širi post i bočni stupci',
        'preview_image': 'blog/images/design-previews/classic_right.png',
    },
    'ponocna_elegancija': {
        'label': 'Ponoćna elegancija',
        'description': 'Tamni elegantni dizajn sa zvjezdanim nebom, šumom i profinjenim svijetlim boxevima',
        'preview_image': 'blog/images/design-previews/ponocna_elegancija.png',
    },
    'ruzicasti_vrt': {
        'label': 'Ružičasti vrt',
        'description': 'Romantični dizajn s ružama, poluprozirnim boxevima i blagim blur efektom pozadine',
        'preview_image': 'blog/images/design-previews/ruzicasti_vrt.jpg',
    },
    'stara_aleja': {
        'label': 'Stara aleja',
        'description': 'Vintage tematski dizajn sa starinskom ulicom, toplim tonovima i elegantnim svijetlim boxevima',
        'preview_image': 'blog/images/design-previews/stara_aleja.jpg',
    },
    'staza_prema_vrhovima': {
        'label': 'Staza prema vrhovima',
        'description': 'Putopisni dizajn s planinarskom stazom, pogledom na planine i toplim večernjim svjetlom',
        'preview_image': 'blog/images/design-previews/staza_prema_vrhovima.png',
    },
    'jedro_u_suton': {
        'label': 'Jedro u suton',
        'description': 'Putopisni tematski dizajn s jedrilicom, zalaskom sunca i jedinstvenim prozirnim panelom za postove i boxeve',
        'preview_image': 'blog/images/design-previews/jedro_u_suton.png',
    },
    'dimni_akordi': {
        'label': 'Dimni akordi',
        'description': 'Gradijalni dizajn u toplim bakrenim tonovima inspiriran zadimljenim barom i svjetlom s fotografije.',
        'preview_image': 'blog/images/design-previews/dimni_akordi.png',
    },
    'sjene_ulice': {
        'label': 'Sjene ulice',
        'description': 'Gradijentni noir dizajn s noćnom ulicom, prijelazom iz slike u tamnu pozadinu i toplim lampama.',
        'preview_image': 'blog/images/design-previews/sjene_ulice.png',
    },
    'mjesecev_ples': {
        'label': 'Mjesečev ples',
        'description': 'Gradijentni mistični dizajn s mjesečevim nebom, siluetom i prijelazom u tamni zemljani donji dio.',
        'preview_image': 'blog/images/design-previews/mjesecev_ples.png',
    },
    'asfaltni_plamen': {
        'label': 'Asfaltni plamen',
        'description': 'Gradijentni dizajn s crnim muscle autom, dimom i toplim jantarnim prijelazom u tamni donji dio.',
        'preview_image': 'blog/images/design-previews/asfaltni_plamen.png',
    },
    'misticno_jezero': {
        'label': 'Mistično jezero',
        'description': 'Mistični ljubičasti dizajn s čamcem, lampionima, vodopadom i blagim svjetlucavim efektom.',
        'preview_image': 'blog/images/design-previews/misticno_jezero.jpg',
    },
}

DESIGN_TEMPLATE_LABELS = {
    key: value['label']
    for key, value in DESIGN_TEMPLATE_META.items()
}

DESIGN_RIGHT_LAYOUT_TEMPLATES = (
    'default_right',
    'dark_right',
    'classic_right',
)


def get_design_templates():
    return [
        {
            'value': key,
            **value,
        }
        for key, value in DESIGN_TEMPLATE_META.items()
    ]


DESIGN_RESET_FIELDS = {
    'blog_title': ('blog_title_font', 'blog_title_color'),
    'post_title': ('post_title_font', 'post_title_color'),
    'box_title': ('box_title_font', 'box_title_color'),
}


def normalize_user_boxes(user):
    for position in ('left', 'right'):
        boxes = UserBox.objects.filter(user=user, position=position).order_by('order', 'id')
        for index, box in enumerate(boxes):
            if box.order != index:
                box.order = index
                box.save(update_fields=['order'])


def get_next_box_order(user, position):
    current_max = UserBox.objects.filter(user=user, position=position).order_by('-order').values_list('order', flat=True).first()
    if current_max is None:
        return 0
    return current_max + 1


def validate_box_layout_counts(layout_items):
    left_count = sum(1 for item in layout_items if item.get('position') == 'left')
    right_count = sum(1 for item in layout_items if item.get('position') == 'right')

    if left_count > MAX_BOXES_PER_SIDE or right_count > MAX_BOXES_PER_SIDE:
        return False

    return True


def validate_blog_banner(upload):
    if not upload:
        return None

    if upload.size > MAX_BLOG_BANNER_SIZE:
        return 'Banner slika je prevelika. Maksimalna veličina je 2 MB.'

    try:
        image = Image.open(upload)
        width, height = image.size
        upload.seek(0)
    except (UnidentifiedImageError, OSError, ValueError):
        try:
            upload.seek(0)
        except Exception:
            pass
        return 'Banner slika nije ispravna slikovna datoteka.'

    if width > MAX_BLOG_BANNER_WIDTH or height > MAX_BLOG_BANNER_HEIGHT:
        return (
            'Banner slika je prevelikih dimenzija. '
            f'Maksimalno je dopušteno {MAX_BLOG_BANNER_WIDTH} x {MAX_BLOG_BANNER_HEIGHT} px.'
        )

    return None


def _normalize_publish_at(value):
    if not value:
        return None
    try:
        parsed = timezone.datetime.strptime(value, '%Y-%m-%dT%H:%M')
    except (TypeError, ValueError):
        return None
    return timezone.make_aware(parsed, timezone.get_current_timezone())


def _apply_publication_mode_to_post(post, publication_mode, publish_at):
    if publication_mode == 'scheduled':
        post.status = 'scheduled'
        post.publish_at = publish_at
    elif publication_mode == 'draft':
        post.status = 'draft'
        post.publish_at = None
    else:
        post.status = 'published'
        post.publish_at = None


def _first_form_error(form, default_message='Molimo popunite sva obavezna polja.'):
    for field_errors in form.errors.values():
        if field_errors:
            return field_errors[0]
    return default_message


@staff_member_required
def update_site_message(request):
    if not (request.user.is_authenticated and request.user.is_superuser):
        return HttpResponseForbidden('Nemaš ovlasti.')

    if request.method == 'POST':
        
        msg, _ = SiteMessage.objects.get_or_create(id=1)
        msg.content_html = request.POST.get('content_html', '')
        if request.POST.get('remove_image') == '1' and msg.image:
            msg.image.delete(save=False)
            msg.image = None
        if 'image' in request.FILES:
            msg.image = request.FILES['image']
        msg.save()
        messages.success(request, 'Poruka je spremljena.')
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def add_box(request):
    normalize_user_boxes(request.user)
    left_count = UserBox.objects.filter(user=request.user, position='left').count()
    right_count = UserBox.objects.filter(user=request.user, position='right').count()

    if request.method == 'POST':
        form = UserBoxForm(request.POST)
        if form.is_valid():
            position = form.cleaned_data['position']

            if position == 'left' and left_count >= MAX_BOXES_PER_SIDE:
                messages.error(request, f'Ne možeš dodati više od {MAX_BOXES_PER_SIDE} lijeva boxa.')
                return redirect('/blog/settings/?tab=boxevi')

            if position == 'right' and right_count >= MAX_BOXES_PER_SIDE:
                messages.error(request, f'Ne možeš dodati više od {MAX_BOXES_PER_SIDE} desna boxa.')
                return redirect('/blog/settings/?tab=boxevi')

            box = form.save(commit=False)
            box.user = request.user
            box.order = get_next_box_order(request.user, position)
            box.save()
            return redirect(f'/blog/settings/?tab=boxevi&box={box.id}')
    else:
        form = UserBoxForm()

    return render(request, 'blog/add_box.html', {
        'form': form,
        'left_count': left_count,
        'right_count': right_count,
        'max_boxes_per_side': MAX_BOXES_PER_SIDE,
        'box_title_limit': UserBoxForm.MAX_TITLE_LENGTH,
        'box_content_limit': UserBoxForm.MAX_CONTENT_LENGTH,
    })


@login_required
def edit_box(request, box_id):
    normalize_user_boxes(request.user)
    box = get_object_or_404(UserBox, id=box_id, user=request.user)

    if request.method == 'POST':
        form = UserBoxForm(request.POST, instance=box)
        if form.is_valid():
            new_position = form.cleaned_data.get('position')
            old_position = box.position

            left_count = UserBox.objects.filter(user=request.user, position='left').exclude(id=box.id).count()
            right_count = UserBox.objects.filter(user=request.user, position='right').exclude(id=box.id).count()

            if new_position == 'left' and left_count >= MAX_BOXES_PER_SIDE:
                messages.error(request, f'Ne možeš prebaciti box lijevo jer je lijeva strana puna (max {MAX_BOXES_PER_SIDE}).')
                return redirect(f'/blog/settings/?tab=boxevi&box={box.id}')

            if new_position == 'right' and right_count >= MAX_BOXES_PER_SIDE:
                messages.error(request, f'Ne možeš prebaciti box desno jer je desna strana puna (max {MAX_BOXES_PER_SIDE}).')
                return redirect(f'/blog/settings/?tab=boxevi&box={box.id}')

            updated_box = form.save(commit=False)

            if old_position != new_position:
                updated_box.order = get_next_box_order(request.user, new_position)

            updated_box.save()
            normalize_user_boxes(request.user)
            return redirect(f'/blog/settings/?tab=boxevi&box={box.id}')

        for field_errors in form.errors.values():
            for error in field_errors:
                messages.error(request, error)

        return redirect(f'/blog/settings/?tab=boxevi&box={box.id}')
    else:
        form = UserBoxForm(instance=box)

    return render(request, 'blog/edit_box.html', {'form': form})


@login_required
def delete_box(request, box_id):
    box = get_object_or_404(UserBox, id=box_id, user=request.user)
    if request.method == 'POST':
        box.delete()
        normalize_user_boxes(request.user)
        return redirect('/blog/settings/?tab=boxevi')
    return render(request, 'blog/delete_box.html', {'box': box})


@login_required
def blog_settings(request):
    publish_due_posts(request.user)
    profile = request.user.profile
    normalize_user_boxes(request.user)
    boxes = UserBox.objects.filter(user=request.user).order_by('position', 'order', 'id')
    left_boxes = list(boxes.filter(position='left'))
    right_boxes = list(boxes.filter(position='right'))
    left_count = len(left_boxes)
    right_count = len(right_boxes)
    box_id = request.GET.get('box')
    active_box = boxes.filter(id=box_id).first() if box_id else boxes.first()
    active_box_form = UserBoxForm(instance=active_box) if active_box else None

    post_filter = request.GET.get('post_filter', 'published')
    post_id = request.GET.get('post_id')
    edit_post = None
    user_posts = None
    post_form = PostForm()

    settings_tab = request.GET.get('settings_tab', 'opcenito')
    design_tab = request.GET.get('design_tab', 'predlosci')

    blocked_users = (
        UserBlock.objects
        .filter(blocker=request.user)
        .select_related("blocked", "blocked__profile")
        .order_by("blocked__username")
    )

    restricted_users = (
        UserRestriction.objects
        .filter(owner=request.user)
        .select_related("restricted", "restricted__profile")
        .order_by("restricted__username")
    )

    if request.method == 'POST':

                # --- ODBLOKIRAJ KORISNIKA ---
        if "unblock_user_id" in request.POST:
            unblock_user_id = request.POST.get("unblock_user_id")

            block_relation = (
                UserBlock.objects
                .filter(blocker=request.user, blocked_id=unblock_user_id)
                .select_related("blocked")
                .first()
            )

            if block_relation:
                blocked_username = block_relation.blocked.username
                block_relation.delete()
                messages.success(request, f"Odblokirao si korisnika {blocked_username}.")
            else:
                messages.error(request, "Korisnik nije pronađen u listi blokiranih.")

            return redirect("/blog/settings/?tab=postavke&settings_tab=sigurnost")

        if "remove_restriction_user_id" in request.POST:
            restricted_user_id = request.POST.get("remove_restriction_user_id")

            restriction_relation = (
                UserRestriction.objects
                .filter(owner=request.user, restricted_id=restricted_user_id)
                .select_related("restricted")
                .first()
            )

            if restriction_relation:
                restricted_username = restriction_relation.restricted.username
                restriction_relation.delete()
                messages.success(request, f"Maknuo si ograničenje za korisnika {restricted_username}.")
            else:
                messages.error(request, "Korisnik nije pronađen u listi ograničenih.")

            return redirect("/blog/settings/?tab=postavke&settings_tab=sigurnost")

        if 'save_box_layout' in request.POST:
            raw_layout = request.POST.get('box_layout_json', '[]')

            try:
                layout = json.loads(raw_layout)
            except json.JSONDecodeError:
                messages.error(request, 'Raspored boxeva nije ispravan.')
                return redirect('/blog/settings/?tab=boxevi')

            if not isinstance(layout, list):
                messages.error(request, 'Raspored boxeva nije ispravan.')
                return redirect('/blog/settings/?tab=boxevi')

            cleaned_layout = []
            seen_ids = set()
            user_box_ids = set(UserBox.objects.filter(user=request.user).values_list('id', flat=True))

            for item in layout:
                if not isinstance(item, dict):
                    continue

                try:
                    box_id = int(item.get('id'))
                except (TypeError, ValueError):
                    continue

                position = item.get('position')
                if position not in {'left', 'right'}:
                    continue

                if box_id in seen_ids or box_id not in user_box_ids:
                    continue

                seen_ids.add(box_id)
                cleaned_layout.append({'id': box_id, 'position': position})

            if len(cleaned_layout) != len(user_box_ids):
                messages.error(request, 'Nisu spremljeni svi boxevi. Pokušaj ponovno.')
                return redirect('/blog/settings/?tab=boxevi')

            if not validate_box_layout_counts(cleaned_layout):
                messages.error(request, f'Na svakoj strani mogu biti najviše {MAX_BOXES_PER_SIDE} boxa.')
                return redirect('/blog/settings/?tab=boxevi')

            grouped = {'left': [], 'right': []}
            for item in cleaned_layout:
                grouped[item['position']].append(item['id'])

            for position in ('left', 'right'):
                for order, box_id in enumerate(grouped[position]):
                    UserBox.objects.filter(id=box_id, user=request.user).update(position=position, order=order)

            normalize_user_boxes(request.user)

            target_box_id = request.POST.get('active_box_id')
            if target_box_id and str(target_box_id).isdigit() and int(target_box_id) in user_box_ids:
                messages.success(request, 'Raspored boxeva je spremljen.')
                return redirect(f'/blog/settings/?tab=boxevi&box={int(target_box_id)}')

            messages.success(request, 'Raspored boxeva je spremljen.')
            return redirect('/blog/settings/?tab=boxevi')

        if 'bulk_restore' in request.POST or 'bulk_permanent_delete' in request.POST:
            selected_ids = request.POST.getlist('selected_posts')
            if not selected_ids:
                messages.error(request, 'Niste označili nijedan post.')
                return redirect('/blog/settings/?tab=postovi&post_filter=deleted')
            posts_qs = Post.objects.filter(id__in=selected_ids, author=request.user, status='deleted')
            if 'bulk_restore' in request.POST:
                posts_qs.update(status='draft')
                return redirect('/blog/settings/?tab=postovi&post_filter=draft')
            for post in posts_qs:
                if post.image:
                    post.image.delete(save=False)
                for img in post.images.all():
                    if img.image:
                        img.image.delete(save=False)
                    img.delete()
                post.delete()
            return redirect('/blog/settings/?tab=postovi&post_filter=deleted')

        if 'create_quiz' in request.POST or 'save_quiz_draft' in request.POST:
            question = request.POST.get('question', '').strip()
            options = [o.strip() for o in request.POST.getlist('quiz_option') if o.strip()]
            correct_index = request.POST.get('correct_option')
            if not question:
                messages.error(request, 'Pitanje je obavezno.')
                return redirect('/blog/settings/?tab=postovi&post_filter=quiz_new')
            if len(options) < 2:
                messages.error(request, 'Dodaj barem 2 odgovora.')
                return redirect('/blog/settings/?tab=postovi&post_filter=quiz_new')
            if correct_index in (None, ''):
                messages.error(request, 'Moraš označiti točan odgovor.')
                return redirect('/blog/settings/?tab=postovi&post_filter=quiz_new')
            correct_index = int(correct_index)
            category = Category.objects.filter(name__iexact='Kviz').first()
            if not category:
                messages.error(request, 'Ne postoji kategorija "Kviz".')
                return redirect('/blog/settings/?tab=postovi&post_filter=quiz_new')
            status = 'published' if 'create_quiz' in request.POST else 'draft'
            post = Post.objects.create(author=request.user, title=question, content='', status=status, category=category, post_type='quiz')
            if request.FILES.get('image'):
                post.image = request.FILES['image']
            if status == 'published':
                assign_home_image(post)
            post.save()
            for i, text in enumerate(options):
                QuizOption.objects.create(post=post, text=text, is_correct=(i == correct_index))
            return redirect(f'/blog/settings/?tab=postovi&post_filter={status}')

        if 'create_poll' in request.POST or 'save_poll_draft' in request.POST:
            question = request.POST.get('question', '').strip()
            options = [o.strip() for o in request.POST.getlist('poll_option') if o.strip()]
            if not question:
                messages.error(request, 'Pitanje ankete je obavezno.')
                return redirect('/blog/settings/?tab=postovi&post_filter=poll_new')
            if len(options) < 2:
                messages.error(request, 'Dodaj barem 2 opcije.')
                return redirect('/blog/settings/?tab=postovi&post_filter=poll_new')
            category = Category.objects.filter(name__iexact='Anketa').first()
            if not category:
                messages.error(request, 'Ne postoji kategorija "Anketa".')
                return redirect('/blog/settings/?tab=postovi&post_filter=poll_new')
            status = 'published' if 'create_poll' in request.POST else 'draft'
            post = Post.objects.create(author=request.user, title=question, content='', status=status, category=category, post_type='poll')
            if request.FILES.get('image'):
                post.image = request.FILES['image']
            if status == 'published':
                assign_home_image(post)
            post.save()
            for text in options:
                PollOption.objects.create(post=post, text=text)
            return redirect(f'/blog/settings/?tab=postovi&post_filter={status}')

        if 'permanent_delete_id' in request.POST:
            post = Post.objects.filter(id=request.POST.get('permanent_delete_id'), author=request.user).first()
            if post:
                if post.image:
                    post.image.delete(save=False)
                for img in post.images.all():
                    if img.image:
                        img.image.delete(save=False)
                    img.delete()
                post.delete()
            return redirect('/blog/settings/?tab=postovi&post_filter=deleted')

        if 'restore_post_id' in request.POST:
            post = Post.objects.filter(id=request.POST.get('restore_post_id'), author=request.user).first()
            if post:
                post.status = 'draft'
                post.save()
            return redirect('/blog/settings/?tab=postovi&post_filter=draft')

        if 'delete_post_id' in request.POST:
            post = Post.objects.filter(id=request.POST.get('delete_post_id'), author=request.user).first()
            if post:
                post.status = 'deleted'
                post.save()
            return redirect('/blog/settings/?tab=postovi&post_filter=published')

        if 'update_post_id' in request.POST:
            post = Post.objects.filter(id=request.POST.get('update_post_id'), author=request.user).first()
            if post:
                form = PostForm(request.POST, request.FILES, instance=post)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.category = Category.objects.filter(id=request.POST.get('category')).first()
                    post.allow_comments = form.cleaned_data.get('allow_comments', True)
                    publication_mode = form.cleaned_data.get('publication_mode', 'published')
                    publish_at = form.cleaned_data.get('publish_at')
                    if request.POST.get('delete_image') and post.image:
                        post.image.delete(save=False)
                        post.image = None
                    _apply_publication_mode_to_post(post, publication_mode, publish_at)
                    if post.status == 'published':
                        assign_home_image(post)
                    delete_ids = request.POST.getlist('delete_post_images')
                    if delete_ids:
                        imgs = PostImage.objects.filter(id__in=delete_ids, post=post)
                        for img in imgs:
                            if img.image:
                                img.image.delete(save=False)
                            img.delete()
                    post.save()
                    apply_tags_to_post(post, form.cleaned_data.get('tags_list', []))
                    for upload in request.FILES.getlist('images'):
                        PostImage.objects.create(post=post, image=upload)
                    return redirect(f'/blog/settings/?tab=postovi&post_filter={post.status}')
                messages.error(request, _first_form_error(form))
                return redirect(f'/blog/settings/?tab=postovi&post_filter=edit&post_id={post.id}')

        if 'publish_post' in request.POST or 'save_draft' in request.POST or 'schedule_post' in request.POST:
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.category = Category.objects.filter(id=request.POST.get('category')).first()
                post.post_type = 'post'
                post.allow_comments = form.cleaned_data.get('allow_comments', True)

                if 'schedule_post' in request.POST:
                    publication_mode = 'scheduled'
                elif 'save_draft' in request.POST:
                    publication_mode = 'draft'
                else:
                    publication_mode = 'published'

                publish_at = form.cleaned_data.get('publish_at')
                _apply_publication_mode_to_post(post, publication_mode, publish_at)

                if post.status == 'published' and not post.category:
                    messages.error(request, 'Morate odabrati kategoriju prije objave.')
                    post_filter = 'new'
                    post_form = form
                else:
                    if post.status == 'published':
                        assign_home_image(post)
                    post.save()
                    apply_tags_to_post(post, form.cleaned_data.get('tags_list', []))
                    for upload in request.FILES.getlist('images'):
                        PostImage.objects.create(post=post, image=upload)
                    return redirect(f'/blog/settings/?tab=postovi&post_filter={post.status}')
            else:
                messages.error(request, _first_form_error(form))
                post_filter = 'new'
                post_form = form

        if 'design' in request.POST:
            selected_design = request.POST.get('design')
            if selected_design in dict(Profile.TEMPLATE_CHOICES):
                profile.template = selected_design
                profile.save()
            return redirect('/blog/settings/?tab=dizajn&design_tab=predlosci')

        if 'save_design_customization' in request.POST:
            active_template = profile.template if profile.template in DESIGN_TEMPLATE_LABELS else 'default'
            current_preferences = get_blog_preferences(request.user)
            design_customizations = normalize_design_customizations(
                current_preferences.get('design_customizations')
            )
            current_design = design_customizations.get(active_template, {}).copy()
            default_designs = normalize_design_customizations(None)
            reset_part = request.POST.get('reset_design_part')

            if reset_part in DESIGN_RESET_FIELDS:
                for field_name in DESIGN_RESET_FIELDS[reset_part]:
                    current_design[field_name] = default_designs[active_template][field_name]
                messages.success(request, 'Odabrani naslov je vraćen na zadani izgled.')
            else:
                for field_name in (
                    'blog_title_font',
                    'post_title_font',
                    'box_title_font',
                    'blog_title_color',
                    'post_title_color',
                    'box_title_color',
                    'right_box_columns',
                ):
                    if field_name in request.POST:
                        current_design[field_name] = request.POST.get(field_name)

                messages.success(request, 'Uređivanje dizajna je spremljeno.')

            design_customizations[active_template] = current_design
            set_blog_preferences(request.user, {
                'design_customizations': design_customizations,
            })
            return redirect('/blog/settings/?tab=dizajn&design_tab=uredivanje')

        if request.GET.get('tab') == 'postavke':
            settings_changed = False
            banner_changed = False
            selected_position = request.POST.get('blog_banner_position')
            if selected_position in {'left', 'center', 'right'} and profile.blog_banner_position != selected_position:
                profile.blog_banner_position = selected_position
                banner_changed = True
                settings_changed = True

            updated_preferences = {}

            posts_per_page = request.POST.get('posts_per_page')
            if posts_per_page in {'5', '10', '15', '20'}:
                updated_preferences['posts_per_page'] = int(posts_per_page)

            archive_mode = request.POST.get('blog_archive_mode')
            if archive_mode in {'both', 'calendar', 'list', 'none'}:
                updated_preferences['blog_archive_mode'] = archive_mode

            updated_preferences['show_post_tags'] = True
            updated_preferences['show_post_comments'] = request.POST.get('show_post_comments', '1') == '1'
            updated_preferences['allow_comments'] = request.POST.get('allow_comments', '1') == '1'
            set_blog_preferences(request.user, updated_preferences)
            settings_changed = True

            allow_anonymous_comments = request.POST.get('allow_anonymous_comments', '0') == '1'
            current_allow_anonymous = get_allow_anonymous_comments(request.user)
            if current_allow_anonymous != allow_anonymous_comments:
                set_allow_anonymous_comments(request.user, allow_anonymous_comments)

            if request.POST.get('delete_blog_banner') == '1':
                if profile.blog_banner:
                    profile.blog_banner.delete(save=False)
                profile.blog_banner = None
                banner_changed = True
                settings_changed = True

            if request.FILES.get('blog_banner'):
                new_banner = request.FILES['blog_banner']
                banner_error = validate_blog_banner(new_banner)
                if banner_error:
                    messages.error(request, banner_error)
                    return redirect(f'/blog/settings/?tab=postavke&settings_tab={settings_tab}')

                if profile.blog_banner and profile.blog_banner.name:
                    profile.blog_banner.delete(save=False)
                profile.blog_banner = new_banner
                banner_changed = True
                settings_changed = True

            if settings_changed:
                profile.save()
                if banner_changed:
                    messages.success(request, 'Postavke i slika na vrhu bloga su spremljene.')
                else:
                    messages.success(request, 'Postavke bloga su spremljene.')
                return redirect(f'/blog/settings/?tab=postavke&settings_tab={settings_tab}')

        if request.POST.get('cropped_image'):
            image_format, imgstr = request.POST['cropped_image'].split(';base64,')
            ext = image_format.split('/')[-1]
            file = ContentFile(base64.b64decode(imgstr), name=f'avatar.{ext}')
            if profile.avatar and profile.avatar.path and os.path.isfile(profile.avatar.path):
                os.remove(profile.avatar.path)
            profile.avatar = file
            profile.save()
            return redirect('user_blog', username=request.user.username)

    if post_filter == 'edit' and post_id:
        edit_post = Post.objects.filter(id=post_id, author=request.user).first()
    if edit_post:
        post_form = PostForm(instance=edit_post)

    if post_filter == 'published':
        user_posts = Post.objects.filter(author=request.user, status='published').order_by('-created_at')
    elif post_filter == 'draft':
        user_posts = Post.objects.filter(author=request.user, status='draft').order_by('-created_at')
    elif post_filter == 'scheduled':
        user_posts = Post.objects.filter(author=request.user, status='scheduled').order_by('publish_at', '-created_at')
    elif post_filter == 'deleted':
        user_posts = Post.objects.filter(author=request.user, status='deleted').order_by('-created_at')

    blog_preferences = apply_blog_preferences_to_profile(profile, request.user)
    design_customizations = blog_preferences.get('design_customizations', {})
    active_design_template = profile.template if profile.template in DESIGN_TEMPLATE_LABELS else 'default'
    active_design_customization = build_design_customization_payload(
        design_customizations.get(
            active_design_template,
            blog_preferences.get('active_design_customization', {}),
        )
    )

    return render(request, 'blog/blog_settings.html', {
        'boxes': boxes,
        'left_boxes': left_boxes,
        'right_boxes': right_boxes,
        'left_count': left_count,
        'right_count': right_count,
        'max_boxes_per_side': MAX_BOXES_PER_SIDE,
        'box_title_limit': UserBoxForm.MAX_TITLE_LENGTH,
        'box_content_limit': UserBoxForm.MAX_CONTENT_LENGTH,
        'active_box': active_box,
        'active_box_form': active_box_form,
        'profile': profile,
        'user_posts': user_posts,
        'post_filter': post_filter,
        'edit_post': edit_post,
        'categories': Category.objects.all().order_by('group', 'name'),
        'published_count': Post.objects.filter(author=request.user, status='published').count(),
        'draft_count': Post.objects.filter(author=request.user, status='draft').count(),
        'scheduled_count': Post.objects.filter(author=request.user, status='scheduled').count(),
        'deleted_count': Post.objects.filter(author=request.user, status='deleted').count(),
        'post_form': post_form,
        "blocked_users": blocked_users,
        "restricted_users": restricted_users,
        'settings_tab': settings_tab,
        'design_tab': design_tab,
        'design_font_choices': get_design_font_choices(),
        'design_template_labels': DESIGN_TEMPLATE_LABELS,
        'design_templates': get_design_templates(),
        'design_right_layout_templates': DESIGN_RIGHT_LAYOUT_TEMPLATES,
        'active_design_template': active_design_template,
        'active_design_customization': active_design_customization,
        'allow_anonymous_comments': get_allow_anonymous_comments(request.user),
        'blog_preferences': blog_preferences,
    })