from django import forms
from django.conf import settings
from django.utils import timezone
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from ckeditor.widgets import CKEditorWidget
import re
from .models import Category, Post, Comment, Profile, UserBox, BugReport, AuthorQuestion, extract_youtube_video_id
from .html_sanitizer import sanitize_post_html


class PostForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all().order_by("group", "name", "id"),
        required=False,
        empty_label="Odaberi kategoriju",
        label="Kategorija",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    tags_input = forms.CharField(
        required=False,
        label="Tagovi",
        help_text="Odvoji zarezom. Bez razmaka. Dopušteno: slova, brojevi i _. Primjer: ljubav, film_serije, co2",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "npr. ljubav, film_serije, co2"
        })
    )

    video_url = forms.URLField(
        required=False,
        label="YouTube video link",
        widget=forms.URLInput(attrs={
            "class": "form-control",
            "placeholder": "https://www.youtube.com/watch?v=..."
        })
    )

    content = forms.CharField(
        widget=CKEditorWidget(config_name="minimal")
    )

    allow_comments = forms.BooleanField(
        required=False,
        initial=True,
        label="Dopusti komentare na ovom postu"
    )

    publication_mode = forms.ChoiceField(
        label="Objava",
        choices=(
            ("published", "Objavi odmah"),
            ("draft", "Spremi kao skicu"),
            ("scheduled", "Objavi kasnije"),
        ),
        initial="published",
        required=False,
        widget=forms.HiddenInput()
    )

    publish_at = forms.DateTimeField(
        required=False,
        label="Datum i vrijeme objave",
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            attrs={"class": "form-control", "type": "datetime-local"},
            format="%Y-%m-%dT%H:%M"
        )
    )

    class Meta:
        model = Post
        fields = ["title", "category", "content", "image", "video_url", "allow_comments", "publish_at"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["category"].widget.attrs.update({"class": "form-select"})
        self.fields["image"].widget.attrs.update({"class": "form-control"})
        self.fields["video_url"].widget.attrs.update({"class": "form-control"})
        self.fields["allow_comments"].widget.attrs.update({"class": "form-check-input"})

        if self.instance and getattr(self.instance, "pk", None):
            try:
                existing = list(self.instance.tags.all().values_list("name", flat=True))
                if existing:
                    self.fields["tags_input"].initial = ", ".join(existing)
            except Exception:
                pass

            if self.instance.status == "scheduled":
                self.fields["publication_mode"].initial = "scheduled"
            elif self.instance.status == "draft":
                self.fields["publication_mode"].initial = "draft"
            else:
                self.fields["publication_mode"].initial = "published"

            if self.instance.publish_at:
                local_publish_at = timezone.localtime(self.instance.publish_at)
                self.initial["publish_at"] = local_publish_at.strftime("%Y-%m-%dT%H:%M")
        else:
            self.fields["publication_mode"].initial = "published"

    def clean_tags_input(self):
        raw = (self.cleaned_data.get("tags_input") or "").strip()
        if not raw:
            self.cleaned_data["tags_list"] = []
            return ""

        parts = [p.strip() for p in raw.split(",") if p.strip()]

        if len(parts) > 5:
            raise forms.ValidationError("Možeš staviti najviše 5 tagova.")

        allowed = re.compile(r"^[A-Za-z0-9_ČĆĐŠŽčćđšž]+$")

        cleaned = []
        seen = set()

        for t in parts:
            if " " in t:
                raise forms.ValidationError("Tag mora biti jedna riječ (bez razmaka).")

            if not allowed.match(t):
                raise forms.ValidationError("Tag smije sadržavati samo slova, brojeve i znak _.")

            if t.startswith("_") or t.endswith("_"):
                raise forms.ValidationError("Tag ne smije početi ili završiti s _.")

            if "__" in t:
                raise forms.ValidationError("Tag ne smije imati dva '_' zaredom (__).")

            t_norm = t.lower()

            if len(t_norm) < 2 or len(t_norm) > 30:
                raise forms.ValidationError("Tag mora imati 2 do 30 znakova.")

            if t_norm not in seen:
                seen.add(t_norm)
                cleaned.append(t_norm)

        self.cleaned_data["tags_list"] = cleaned
        return raw

    def clean_video_url(self):
        url = (self.cleaned_data.get("video_url") or "").strip()

        if not url:
            return ""

        if not extract_youtube_video_id(url):
            raise forms.ValidationError("Upiši ispravan YouTube link.")

        return url

    def clean_content(self):
        content = self.cleaned_data.get("content") or ""
        cleaned_content = sanitize_post_html(content)
        plain_text = strip_tags(cleaned_content).replace(" ", " ").strip()

        if not plain_text:
            raise forms.ValidationError("Sadržaj posta je obavezan.")

        return cleaned_content


    def clean(self):
        cleaned_data = super().clean()
        publish_at = cleaned_data.get("publish_at")

        if publish_at and timezone.is_naive(publish_at):
            publish_at = timezone.make_aware(publish_at, timezone.get_current_timezone())

        if publish_at:
            if publish_at <= timezone.now():
                self.add_error("publish_at", "Vrijeme objave mora biti u budućnosti ili ostavi polje prazno za objavu odmah.")
            cleaned_data["publish_at"] = publish_at

        return cleaned_data



class CommentForm(forms.ModelForm):
    anonymous = forms.BooleanField(required=False, label="Objavi anonimno")

    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Napiši komentar..."
            }),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ovaj email već postoji.")
        return email


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["blog_name", "blog_tagline"]
        widgets = {
            "blog_name": forms.TextInput(attrs={"class": "form-control"}),
            "blog_tagline": forms.TextInput(attrs={
                "class": "form-control",
                "maxlength": "220",
                "placeholder": "Kratka poruka ispod naslova bloga",
            }),
        }


class AuthorProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "author_bio",
            "author_full_name",
            "author_nickname",
            "author_birth_date",
            "author_birth_place",
            "author_education",
            "author_occupation",
            "author_languages",
            "author_religion",
            "author_nationality",
            "author_hobbies",
            "author_interests",
            "author_favorite_topics",
            "author_inspiration",
            "author_motto",
            "author_contact",
            "author_social_links",
            "author_website",
            "allow_author_questions",
        ]
        widgets = {
            "author_bio": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Napiši nešto o sebi..."
            }),
            "author_full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "npr. Ivana Horvat"}),
            "author_nickname": forms.TextInput(attrs={"class": "form-control", "placeholder": "npr. Iva, MoonlightWriter..."}),
            "author_birth_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "author_birth_place": forms.TextInput(attrs={"class": "form-control", "placeholder": "npr. Split"}),
            "author_education": forms.TextInput(attrs={"class": "form-control", "placeholder": "npr. Fakultet elektrotehnike"}),
            "author_occupation": forms.TextInput(attrs={"class": "form-control", "placeholder": "npr. student, profesor, pisac..."}),
            "author_languages": forms.TextInput(attrs={"class": "form-control", "placeholder": "npr. hrvatski, engleski, njemački"}),
            "author_religion": forms.TextInput(attrs={"class": "form-control", "placeholder": "opcionalno"}),
            "author_nationality": forms.TextInput(attrs={"class": "form-control", "placeholder": "opcionalno"}),
            "author_hobbies": forms.TextInput(attrs={"class": "form-control", "placeholder": "npr. glazba, fotografija, putovanja"}),
            "author_interests": forms.TextInput(attrs={"class": "form-control", "placeholder": "npr. filozofija, tehnologija, poezija"}),
            "author_favorite_topics": forms.TextInput(attrs={"class": "form-control", "placeholder": "O čemu najviše voliš pisati?"}),
            "author_inspiration": forms.TextInput(attrs={"class": "form-control", "placeholder": "Što te najviše inspirira?"}),
            "author_motto": forms.TextInput(attrs={"class": "form-control", "placeholder": "Kratka misao ili moto"}),
            "author_contact": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "npr. email, način kontakta ili kratka napomena"}),
            "author_social_links": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "npr. Instagram: @ime\nYouTube: link\nFacebook: link"}),
            "author_website": forms.TextInput(attrs={"class": "form-control", "placeholder": "npr. https://moj-portfolio.com"}),
            "allow_author_questions": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "author_bio": "Kratka autobiografija",
            "author_full_name": "Ime i prezime",
            "author_nickname": "Nadimak",
            "author_birth_date": "Datum rođenja",
            "author_birth_place": "Mjesto rođenja",
            "author_education": "Obrazovanje",
            "author_occupation": "Zanimanje / posao",
            "author_languages": "Jezici",
            "author_religion": "Religija",
            "author_nationality": "Nacionalnost",
            "author_hobbies": "Hobiji",
            "author_interests": "Interesi",
            "author_favorite_topics": "Omiljene teme o kojima piše",
            "author_inspiration": "Što ga inspirira",
            "author_motto": "Moto",
            "author_contact": "Kontakt",
            "author_social_links": "Društvene mreže",
            "author_website": "Web stranica / portfolio",
            "allow_author_questions": "Dopusti pitanja čitatelja",
        }


class AuthorQuestionForm(forms.ModelForm):
    class Meta:
        model = AuthorQuestion
        fields = ["question"]
        widgets = {
            "question": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Napiši pitanje autoru..."
            }),
        }
        labels = {
            "question": "Pitanje",
        }

    def clean_question(self):
        question = (self.cleaned_data.get("question") or "").strip()
        if len(question) < 3:
            raise forms.ValidationError("Pitanje mora imati barem 3 znaka.")
        if len(question) > 1200:
            raise forms.ValidationError("Pitanje može imati najviše 1200 znakova.")
        return question


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    blog_name = forms.CharField(max_length=200, label="Naziv bloga")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "blog_name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        min_length = getattr(settings, "PASSWORD_MIN_LENGTH", 10)

        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "autocomplete": "username",
        })
        self.fields["email"].widget.attrs.update({
            "class": "form-control",
            "autocomplete": "email",
        })
        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "autocomplete": "new-password",
        })
        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "autocomplete": "new-password",
        })
        self.fields["blog_name"].widget.attrs.update({"class": "form-control"})

        self.fields["password1"].help_text = (
            f"Lozinka mora imati najmanje {min_length} znakova. "
            "Nemoj koristiti samo brojeve, prečestu lozinku ili podatke slične korisničkom imenu."
        )
        self.fields["password2"].help_text = "Ponovno upiši istu lozinku za potvrdu."

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ovaj email već postoji.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            profile = user.profile
            profile.blog_name = self.cleaned_data["blog_name"]
            profile.save()

        return user


class UserBoxForm(forms.ModelForm):
    MAX_TITLE_LENGTH = 80
    MAX_CONTENT_LENGTH = 1200

    content = forms.CharField(
        required=False,
        widget=CKEditorWidget(config_name="minimal")
    )

    class Meta:
        model = UserBox
        fields = ["title", "content", "position"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({
            "class": "form-control",
            "maxlength": str(self.MAX_TITLE_LENGTH),
            "placeholder": "Naslov boxa"
        })
        self.fields["position"].widget.attrs.update({"class": "form-select"})

    def clean_title(self):
        title = (self.cleaned_data.get("title") or "").strip()

        if not title:
            raise forms.ValidationError("Naslov boxa je obavezan.")

        if len(title) > self.MAX_TITLE_LENGTH:
            raise forms.ValidationError(
                f"Naslov može imati najviše {self.MAX_TITLE_LENGTH} znakova."
            )

        return title

    def clean_content(self):
        content = self.cleaned_data.get("content") or ""
        plain_text = strip_tags(content).replace(" ", " ")
        plain_text = re.sub(r"\s+", " ", plain_text).strip()

        if len(plain_text) > self.MAX_CONTENT_LENGTH:
            raise forms.ValidationError(
                f"Tekst može imati najviše {self.MAX_CONTENT_LENGTH} znakova."
            )

        return content


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["blog_name", "blog_tagline", "background_color", "template", "avatar"]


class BugReportForm(forms.ModelForm):
    REQUEST_TYPE_CHOICES = [
        ("kvar", "Kvar"),
        ("pitanje", "Pitanje"),
        ("prijedlog", "Prijedlog"),
    ]

    request_type = forms.ChoiceField(
        choices=REQUEST_TYPE_CHOICES,
        initial="kvar",
        required=False,
        widget=forms.HiddenInput(),
    )
    email = forms.EmailField(
        required=False,
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Email (opcionalno)",
        }),
    )

    class Meta:
        model = BugReport
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Naslov",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Poruka",
            }),
        }
        labels = {
            "title": "Naslov",
            "description": "Poruka",
        }

    def clean_request_type(self):
        value = (self.cleaned_data.get("request_type") or "kvar").strip().lower()
        allowed = {choice[0] for choice in self.REQUEST_TYPE_CHOICES}
        return value if value in allowed else "kvar"
