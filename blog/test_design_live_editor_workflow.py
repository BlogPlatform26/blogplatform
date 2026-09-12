from django.contrib.auth.models import User
from django.test import TestCase
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
