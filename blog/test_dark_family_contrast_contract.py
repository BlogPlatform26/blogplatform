from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class DarkFamilyContrastContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="dark-contrast-author")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Dark contrast",
            content="<p>Sadrzaj</p>",
            status="published",
        )

    def test_dark_variants_render_shared_contrast_contract(self):
        for template in ("dark", "dark_right"):
            self.author.profile.template = template
            self.author.profile.save(update_fields=["template"])
            for url in (
                reverse("user_blog", args=[self.author.username]),
                reverse("post_detail", args=[self.post.pk]),
            ):
                with self.subTest(template=template, url=url):
                    response = self.client.get(url, follow=True)
                    self.assertEqual(response.status_code, 200)
                    content = response.content.decode(response.charset)
                    self.assertIn("Phase 84d: the translucent desktop comment", content)
                    self.assertIn("background:#c92f2f", content)
                    self.assertIn("color:#d9ecff", content)

    def test_unrelated_design_does_not_render_phase84d_contract(self):
        self.author.profile.template = "default"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn(
            "Phase 84d: the translucent desktop comment",
            response.content.decode(response.charset),
        )
