from pathlib import Path

from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
from django.test import TestCase
from django.urls import reverse


class SettingsSidebarMobileContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(
            username="settings-sidebar-owner", password="test-password"
        )

    def test_settings_avatar_and_sidebar_have_scoped_mobile_rules(self):
        self.client.force_login(self.owner)
        response = self.client.get(reverse("blog_settings"), {"tab": "postavke"})
        self.assertEqual(response.status_code, 200)
        content = response.content.decode(response.charset)
        self.assertIn("dashboard-settings-sidebar", content)
        self.assertIn("dashboard-settings-content", content)
        self.assertIn("avatar-upload-field", content)
        self.assertIn("blog/css/blog_settings.css?v=80d", content)

        css_path = finders.find("blog/css/blog_settings.css")
        self.assertIsNotNone(css_path)
        css = Path(css_path).read_text(encoding="utf-8")
        self.assertIn("#avatarForm .avatar-upload-field", css)
        self.assertIn("min-width: 0 !important;", css)
        self.assertIn("(min-width: 768px) and (max-width: 991.98px)", css)
        self.assertIn(".dashboard-settings-sidebar > .list-group", css)
