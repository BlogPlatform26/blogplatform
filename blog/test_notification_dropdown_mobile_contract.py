from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Notification


class NotificationDropdownMobileContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(username="notification-owner", password="test-password")
        cls.sender = User.objects.create_user(username="notification-sender", password="test-password")
        Notification.objects.create(
            recipient=cls.owner,
            sender=cls.sender,
            notification_type="follow",
        )

    def test_both_headers_include_viewport_fitted_mobile_dropdown_rules(self):
        self.client.force_login(self.owner)
        for url in (reverse("notifications"), reverse("edit_profile")):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                html = response.content.decode(response.charset)
                self.assertIn(".bp-final-notification-dropdown", html)
                self.assertIn("position: static !important;", html)
                self.assertIn("left: 10px !important;", html)
                self.assertIn("right: 10px !important;", html)
                self.assertIn("transform: none !important;", html)
                self.assertIn("min-height: 44px !important;", html)
                self.assertContains(response, "notification-sender")
