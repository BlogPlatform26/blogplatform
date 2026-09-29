from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class SimpleFamilyContrastContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="simple-contrast-author")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Simple contrast",
            content="<p>Sadrzaj</p>",
            status="published",
        )

    def test_simple_family_renders_high_contrast_palette_on_blog_and_detail(self):
        expected = {
            "simple_pattern": ("#3d6d86", "#a15e18"),
            "simple_image": ("#3d6d86", "#a15e18"),
            "simple_retro": ("#2f6870", "#2f6870"),
        }
        for template, colors in expected.items():
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
                    self.assertIn("Phase 84c: ordinary simple-family links", content)
                    self.assertIn(colors[0], content)
                    self.assertIn(colors[1], content)

    def test_unrelated_design_does_not_render_phase84c_contract(self):
        self.author.profile.template = "default"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn(
            "Phase 84c: ordinary simple-family links",
            response.content.decode(response.charset),
        )
