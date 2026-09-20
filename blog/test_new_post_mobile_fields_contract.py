from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class NewPostMobileFieldsContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(
            username="new-post-fields-owner", password="test-password"
        )

    def test_new_post_form_has_scoped_mobile_field_rules(self):
        self.client.force_login(self.owner)
        response = self.client.get(
            reverse("blog_settings"), {"tab": "postovi", "post_filter": "new"}
        )
        self.assertEqual(response.status_code, 200)
        content = response.content.decode(response.charset)
        self.assertIn("@media (max-width: 575.98px)", content)
        for selector in (
            "#newPostForm #id_title",
            "#newPostForm #id_video_url",
            "#newPostForm #id_publish_at",
            "#newPostForm #id_tags_input",
            '#newPostForm #newPostImagesWrapper input[type="file"].form-control',
        ):
            with self.subTest(selector=selector):
                self.assertIn(selector, content)
        self.assertIn("min-height: 44px;", content)
        self.assertIn("font-size: 16px;", content)
        self.assertIn("font-size: 14px;", content)
