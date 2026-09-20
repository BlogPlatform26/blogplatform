from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class DesignSettingsMobileTouchContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(username="design-touch-owner", password="test-password")

    def test_design_subtabs_share_scoped_mobile_targets(self):
        self.client.force_login(self.owner)
        for design_tab in ("predlosci", "uredivanje", "ugodaj"):
            with self.subTest(design_tab=design_tab):
                response = self.client.get(
                    reverse("blog_settings"), {"tab": "dizajn", "design_tab": design_tab}
                )
                self.assertEqual(response.status_code, 200)
                html = response.content.decode(response.charset)
                self.assertIn('class="design-settings-scope"', html)
                self.assertIn('blog/css/blog_settings.css', html)
                self.assertIn('?v=80d', html)

        css = (
            Path(settings.BASE_DIR) / "blog" / "static" / "blog" / "css" / "blog_settings.css"
        ).read_text(encoding="utf-8")
        for selector in (
            ".design-settings-scope > .nav-tabs .nav-link",
            '.design-settings-scope > form > button[type="submit"]',
            ".design-settings-scope a.btn",
            ".design-settings-scope .ambience-card .btn",
            ".design-settings-scope .ambience-card .form-select",
        ):
            self.assertIn(selector, css)
        self.assertIn("min-height: 44px !important;", css)
