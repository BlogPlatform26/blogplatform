from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class NewPostMobileActionsContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(
            username="new-post-mobile-owner", password="test-password"
        )

    def test_new_post_tabs_and_actions_have_scoped_mobile_targets(self):
        self.client.force_login(self.owner)
        response = self.client.get(
            reverse("blog_settings"), {"tab": "postovi", "post_filter": "new"}
        )
        self.assertEqual(response.status_code, 200)
        content = response.content.decode(response.charset)
        self.assertIn('class="nav nav-tabs mb-4 post-settings-subtabs"', content)
        self.assertEqual(content.count('href="?tab=postovi&post_filter='), 7)
        self.assertIn("@media (max-width: 575.98px)", content)
        self.assertIn(".post-settings-subtabs .nav-link", content)
        self.assertIn(".new-post-actions .btn", content)
        self.assertIn("min-height: 44px;", content)
        self.assertIn('id="newPostSaveDraftButton"', content)
