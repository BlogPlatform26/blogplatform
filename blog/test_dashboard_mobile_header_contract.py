from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class DashboardMobileHeaderContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(
            username="dashboard-mobile-owner", password="test-password"
        )

    def test_settings_tabs_share_responsive_dashboard_header(self):
        self.client.force_login(self.owner)
        for tab in ("postovi", "boxevi", "dizajn", "autor", "postavke", "statistika"):
            with self.subTest(tab=tab):
                response = self.client.get(reverse("blog_settings"), {"tab": tab})
                self.assertEqual(response.status_code, 200)
                content = response.content.decode(response.charset)
                self.assertIn(
                    '<meta name="viewport" content="width=device-width, initial-scale=1">',
                    content,
                )
                self.assertIn('id="searchToggleBtn"', content)
                self.assertIn('id="navbarSearchInline"', content)
                self.assertIn('id="navbarSearchSubmitBtn"', content)
                self.assertIn("@media (max-width: 991.98px)", content)
                self.assertIn("#navbarSearchInline .input-group", content)
