from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class NewPostMobileToolbarContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(
            username="new-post-toolbar-owner", password="test-password"
        )

    def test_new_post_toolbar_has_mobile_only_touch_rules(self):
        self.client.force_login(self.owner)
        response = self.client.get(
            reverse("blog_settings"), {"tab": "postovi", "post_filter": "new"}
        )
        self.assertEqual(response.status_code, 200)
        content = response.content.decode(response.charset)
        self.assertIn("@media (max-width: 575.98px)", content)
        self.assertIn("#newPostForm .ck-toolbar .ck-button", content)
        self.assertIn(
            "#newPostForm .ck-toolbar .bp-direct-spacing-control select", content
        )
        self.assertIn("min-width: 44px;", content)
        self.assertIn("min-height: 44px;", content)
