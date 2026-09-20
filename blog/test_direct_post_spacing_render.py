from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class DirectPostSpacingRenderTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(username="spacing-owner", password="test-password")
        cls.post = Post.objects.create(
            author=cls.owner, title="Spacing draft", content="<p>Text</p>", status="draft"
        )

    def test_direct_post_forms_include_spacing_assets_once(self):
        self.client.force_login(self.owner)
        for url in (reverse("create_post"), reverse("edit_post", args=[self.post.pk])):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                html = response.content.decode(response.charset)
                self.assertEqual(html.count('id="blogplatformDirectSpacingStyle"'), 1)
                self.assertEqual(html.count('id="blogplatformDirectSpacingScript"'), 1)
                self.assertEqual(html.count('id="blogplatformDisableEditorSpellcheckScript"'), 1)
                self.assertIn('aria-label="Razmak redova"', html)
