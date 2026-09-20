import base64
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from blog.models import Profile, UserBlogPreference
from blog.services import (
    build_design_customization_payload,
    normalize_design_customizations,
    set_blog_preferences,
)


class DesignLiveEditorWorkflowTests(TestCase):
    TITLE_PAYLOAD = {
        "blog_title_font": "arial",
        "blog_title_color": "#123456",
        "blog_title_size": "61",
        "post_title_font": "verdana",
        "post_title_color": "#234567",
        "post_title_size": "37",
        "box_title_font": "garamond",
        "box_title_color": "#345678",
        "box_title_size": "19",
        "post_date_style": "ribbon",
        "post_date_effect": "duo",
        "post_date_color_1": "#456789",
        "post_date_color_2": "#56789a",
        "post_date_size": "123",
    }

    def setUp(self):
        self.temp_media = tempfile.TemporaryDirectory()
        self.media_override = override_settings(MEDIA_ROOT=self.temp_media.name)
        self.media_override.enable()
        self.addCleanup(self.media_override.disable)
        self.addCleanup(self.temp_media.cleanup)
        self.user = User.objects.create_user(
            username="live-editor-user",
            password="test-password",
        )
        self.client.force_login(self.user)
        self.url = reverse("design_live_editor_titles")

    def activate_template(self, template):
        self.user.profile.template = template
        self.user.profile.save(update_fields=["template"])

    def stored_customizations(self, user=None):
        preference = UserBlogPreference.objects.get(user=user or self.user)
        return preference.data["design_customizations"]

    def test_get_is_available_to_authenticated_user(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/design_live_editor.html")
        self.assertContains(response, 'id="designLiveTitlesForm"', html=False)

    def test_mobile_action_targets_are_scoped_to_live_editor(self):
        for template, section in (("magazin", "naslovi"), ("simple_pattern", "pozadine")):
            with self.subTest(template=template, section=section):
                self.activate_template(template)
                response = self.client.get(self.url, {"section": section})
                self.assertEqual(response.status_code, 200)
                html = response.content.decode(response.charset)
                self.assertIn("@media (max-width: 575.98px)", html)
                self.assertIn(".editor-tab-btn,", html)
                self.assertIn(".editor-card-head [data-reset-card],", html)
                self.assertIn(".live-editor-actions button{", html)
                self.assertIn("min-height:44px;", html)

    def test_mobile_field_targets_keep_desktop_rules_unchanged(self):
        for template, section in (("magazin", "naslovi"), ("simple_pattern", "pozadine")):
            with self.subTest(template=template, section=section):
                self.activate_template(template)
                response = self.client.get(self.url, {"section": section})
                self.assertEqual(response.status_code, 200)
                html = response.content.decode(response.charset)
                mobile_rules = html.split("@media (max-width: 575.98px){", 1)[1].split("</style>", 1)[0]
                for selector in (
                    ".editor-card .form-select,",
                    ".editor-card .editor-color-input{",
                    ".editor-card .form-range{",
                ):
                    self.assertIn(selector, mobile_rules)
                self.assertIn("height:44px !important;", mobile_rules)
                self.assertIn("transform:none;", mobile_rules)

    def test_title_save_uses_post_redirect_get_and_persists_all_fields(self):
        self.activate_template("default")

        response = self.client.post(
            self.url,
            {"save_title_settings": "1", **self.TITLE_PAYLOAD},
        )

        self.assertRedirects(
            response,
            self.url + "?section=naslovi",
            fetch_redirect_response=False,
        )
        saved = self.stored_customizations()["default"]
        for field_name, expected in self.TITLE_PAYLOAD.items():
            self.assertEqual(saved[field_name], expected)

    def test_title_save_is_scoped_to_active_template_for_all_registered_designs(self):
        templates = tuple(key for key, _label in Profile.TEMPLATE_CHOICES)
        self.assertEqual(len(templates), 37)

        for index, active_template in enumerate(templates):
            with self.subTest(template=active_template):
                untouched_template = templates[(index + 1) % len(templates)]
                untouched_color = "#abcdef"
                set_blog_preferences(self.user, {
                    "design_customizations": {
                        untouched_template: {"post_title_color": untouched_color},
                    },
                })
                self.activate_template(active_template)

                response = self.client.post(
                    self.url,
                    {"save_title_settings": "1", **self.TITLE_PAYLOAD},
                )

                self.assertEqual(response.status_code, 302)
                saved = self.stored_customizations()
                for field_name, expected in self.TITLE_PAYLOAD.items():
                    self.assertEqual(saved[active_template][field_name], expected)
                self.assertEqual(
                    saved[untouched_template]["post_title_color"],
                    untouched_color,
                )

    def test_saving_second_template_preserves_first_template(self):
        self.activate_template("default")
        self.client.post(
            self.url,
            {"save_title_settings": "1", **self.TITLE_PAYLOAD},
        )

        second_payload = {
            **self.TITLE_PAYLOAD,
            "blog_title_color": "#654321",
            "post_title_color": "#765432",
        }
        self.activate_template("magazin")
        self.client.post(
            self.url,
            {"save_title_settings": "1", **second_payload},
        )

        saved = self.stored_customizations()
        self.assertEqual(saved["default"]["blog_title_color"], "#123456")
        self.assertEqual(saved["default"]["post_title_color"], "#234567")
        self.assertEqual(saved["magazin"]["blog_title_color"], "#654321")
        self.assertEqual(saved["magazin"]["post_title_color"], "#765432")

    def test_two_users_on_same_template_remain_isolated(self):
        second_user = User.objects.create_user(
            username="live-editor-second-user",
            password="test-password",
        )
        second_user.profile.template = "magazin"
        second_user.profile.save(update_fields=["template"])
        set_blog_preferences(second_user, {
            "design_customizations": {
                "magazin": {"post_title_color": "#fedcba"},
            },
        })

        self.activate_template("magazin")
        self.client.post(
            self.url,
            {"save_title_settings": "1", **self.TITLE_PAYLOAD},
        )

        first_saved = self.stored_customizations()["magazin"]
        second_saved = self.stored_customizations(second_user)["magazin"]
        self.assertEqual(first_saved["post_title_color"], "#234567")
        self.assertEqual(second_saved["post_title_color"], "#fedcba")

    def test_reset_all_restores_only_active_template_defaults(self):
        defaults = normalize_design_customizations(None)
        default_active = build_design_customization_payload(defaults["default"])
        set_blog_preferences(self.user, {
            "design_customizations": {
                "default": {"post_title_color": "#111111"},
                "magazin": {"post_title_color": "#222222"},
            },
        })
        self.activate_template("default")

        response = self.client.post(
            self.url,
            {"reset_titles_mode": "all"},
        )

        self.assertRedirects(
            response,
            self.url + "?section=naslovi",
            fetch_redirect_response=False,
        )
        saved = self.stored_customizations()
        title_fields = (
            "blog_title_font", "blog_title_color", "blog_title_size",
            "post_title_font", "post_title_color", "post_title_size",
            "box_title_font", "box_title_color", "box_title_size",
            "post_date_style", "post_date_effect", "post_date_color_1",
            "post_date_color_2", "post_date_size",
        )
        for field_name in title_fields:
            self.assertEqual(saved["default"][field_name], default_active[field_name])
        self.assertEqual(saved["magazin"]["post_title_color"], "#222222")

    def test_bespoke_save_reset_template_and_user_isolation(self):
        active_template = "ponocna_elegancija"
        untouched_template = "ruzicasti_vrt"
        untouched_date = {
            "post_date_style": "soft",
            "post_date_effect": "duo",
            "post_date_color_1": "#112233",
            "post_date_color_2": "#445566",
            "post_date_size": "88",
        }
        set_blog_preferences(self.user, {
            "design_customizations": {untouched_template: untouched_date},
        })
        second_user = User.objects.create_user(
            username="bespoke-isolated-user",
            password="test-password",
        )
        second_user_values = {
            "blog_title_font": "palatino",
            "blog_title_color": "#abcdef",
            "blog_title_size": "52",
            "box_title_font": "times",
            "box_title_color": "#fedcba",
            "box_title_size": "18",
        }
        set_blog_preferences(second_user, {
            "design_customizations": {active_template: second_user_values},
        })
        self.activate_template(active_template)

        response = self.client.post(
            self.url,
            {"save_title_settings": "1", **self.TITLE_PAYLOAD},
        )
        self.assertEqual(response.status_code, 302)
        saved = self.stored_customizations()
        for field_name in (
            "blog_title_font", "blog_title_color", "blog_title_size",
            "box_title_font", "box_title_color", "box_title_size",
            "post_date_style", "post_date_effect", "post_date_color_1",
            "post_date_color_2", "post_date_size",
        ):
            self.assertEqual(saved[active_template][field_name], self.TITLE_PAYLOAD[field_name])
        for field_name, expected in untouched_date.items():
            self.assertEqual(saved[untouched_template][field_name], expected)
        second_saved = self.stored_customizations(second_user)[active_template]
        for field_name, expected in second_user_values.items():
            self.assertEqual(second_saved[field_name], expected)

        response = self.client.post(self.url, {"reset_titles_mode": "all"})
        self.assertEqual(response.status_code, 302)
        saved = self.stored_customizations()
        defaults = build_design_customization_payload(
            normalize_design_customizations(None)[active_template]
        )
        for field_name in (
            "blog_title_font", "blog_title_color", "blog_title_size",
            "box_title_font", "box_title_color", "box_title_size",
            "post_date_style", "post_date_effect", "post_date_color_1",
            "post_date_color_2", "post_date_size",
        ):
            self.assertEqual(saved[active_template][field_name], defaults[field_name])
        for field_name, expected in untouched_date.items():
            self.assertEqual(saved[untouched_template][field_name], expected)
        second_saved = self.stored_customizations(second_user)[active_template]
        for field_name, expected in second_user_values.items():
            self.assertEqual(second_saved[field_name], expected)

    def test_background_editor_is_limited_to_simple_designs(self):
        self.activate_template("default")

        response = self.client.get(self.url + "?section=pozadine")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["supports_background_editor"])
        self.assertEqual(response.context["live_editor_section"], "naslovi")

        response = self.client.post(
            self.url,
            {
                "save_background_settings": "1",
                "outer_background_mode": "color",
                "outer_background_color_1": "#112233",
            },
        )

        self.assertRedirects(
            response,
            self.url + "?section=naslovi",
            fetch_redirect_response=False,
        )
        self.assertFalse(UserBlogPreference.objects.filter(user=self.user).exists())

    def test_pattern_and_retro_background_saves_use_allowed_modes_and_one_header_color(self):
        cases = (
            ("simple_pattern", "gradient"),
            ("simple_retro", "pattern"),
        )

        for template, mode in cases:
            with self.subTest(template=template):
                UserBlogPreference.objects.filter(user=self.user).delete()
                self.activate_template(template)

                response = self.client.post(
                    self.url,
                    {
                        "save_background_settings": "1",
                        "outer_background_mode": mode,
                        "outer_background_color_1": "#112233",
                        "outer_background_color_2": "#445566",
                        "outer_background_pattern": "dots",
                        "outer_background_gradient_direction": "to right",
                        "header_background_mode": "gradient",
                        "header_background_color_1": "#778899",
                        "header_background_color_2": "#aabbcc",
                        "header_background_gradient_direction": "135deg",
                        "content_background_color": "#ddeeff",
                        "box_background_color": "#fedcba",
                    },
                )

                self.assertRedirects(
                    response,
                    self.url + "?section=pozadine",
                    fetch_redirect_response=False,
                )
                saved = self.stored_customizations()[template]
                self.assertEqual(saved["outer_background_mode"], mode)
                self.assertEqual(saved["outer_background_color_1"], "#112233")
                self.assertEqual(saved["outer_background_color_2"], "#445566")
                self.assertEqual(saved["outer_background_pattern"], "dots")
                self.assertEqual(saved["outer_background_gradient_direction"], "to right")
                self.assertEqual(saved["header_background_mode"], "color")
                self.assertEqual(saved["header_background_color_1"], "#778899")
                self.assertEqual(saved["header_background_color_2"], "#778899")
                self.assertEqual(saved["content_background_color"], "#ddeeff")
                self.assertEqual(saved["box_background_color"], "#fedcba")

    def test_simple_image_system_background_preserves_other_template(self):
        set_blog_preferences(self.user, {
            "design_customizations": {
                "simple_pattern": {"outer_background_color_1": "#abcdef"},
            },
        })
        self.activate_template("simple_image")

        response = self.client.post(
            self.url,
            {
                "save_background_settings": "1",
                "outer_background_mode": "system_image",
                "outer_background_color_1": "#102030",
                "outer_background_image": "night_camp",
                "header_background_color_1": "#405060",
                "content_background_color": "#708090",
                "box_background_color": "#a0b0c0",
            },
        )

        self.assertEqual(response.status_code, 302)
        saved = self.stored_customizations()
        self.assertEqual(saved["simple_image"]["outer_background_mode"], "system_image")
        self.assertEqual(saved["simple_image"]["outer_background_image"], "night_camp")
        self.assertEqual(saved["simple_image"]["outer_background_color_1"], "#102030")
        self.assertEqual(saved["simple_pattern"]["outer_background_color_1"], "#abcdef")

    def test_simple_image_upload_delete_and_reset_are_scoped_and_remove_the_file(self):
        png_bytes = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwC"
            "AAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
        )
        upload = SimpleUploadedFile("background.png", png_bytes, content_type="image/png")
        set_blog_preferences(self.user, {
            "design_customizations": {
                "simple_pattern": {"outer_background_color_1": "#abcdef"},
            },
        })
        self.activate_template("simple_image")

        response = self.client.post(
            self.url,
            {
                "save_background_settings": "1",
                "outer_background_mode": "color",
                "outer_background_color_1": "#112233",
                "simple_background_image": upload,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.user.profile.refresh_from_db()
        uploaded_name = self.user.profile.simple_background_image.name
        self.assertTrue(uploaded_name)
        self.assertEqual(
            self.stored_customizations()["simple_image"]["outer_background_mode"],
            "upload_image",
        )

        response = self.client.post(
            self.url,
            {"delete_simple_background_image": "1"},
        )

        self.assertEqual(response.status_code, 302)
        self.user.profile.refresh_from_db()
        self.assertFalse(self.user.profile.simple_background_image)

        response = self.client.post(
            self.url,
            {"reset_background_mode": "all"},
        )

        self.assertEqual(response.status_code, 302)
        saved = self.stored_customizations()
        defaults = normalize_design_customizations(None)["simple_image"]
        for field_name in (
            "outer_background_mode",
            "outer_background_color_1",
            "outer_background_image",
            "header_background_color_1",
            "content_background_color",
            "box_background_color",
        ):
            self.assertEqual(saved["simple_image"][field_name], defaults[field_name])
        self.assertEqual(saved["simple_pattern"]["outer_background_color_1"], "#abcdef")
