from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post
from blog.services import set_blog_preferences


class SimpleRetroHeaderContrastTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase99h_author")
        cls.author.profile.template = "simple_retro"
        cls.author.profile.blog_tagline = "A retro reading room"
        cls.author.profile.save(update_fields=["template", "blog_tagline"])
        cls.post = Post.objects.create(
            author=cls.author,
            title="Retro header contrast",
            content="<p>Content</p>",
            status="published",
        )

    def _public_pages(self):
        return (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        )

    def test_default_retro_header_uses_opaque_dark_teal(self):
        for url in self._public_pages():
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                html = response.content.decode(response.charset)
                self.assertIn("Phase 99h: protect the default retro header", html)
                self.assertIn("color: #244d55 !important", html)
                self.assertIn("opacity: 1", html)

    def test_custom_retro_palette_and_other_template_are_unmodified(self):
        set_blog_preferences(self.author, {
            "design_customizations": {
                "simple_retro": {"header_background_color_1": "#123456"},
            },
        })
        response = self.client.get(self._public_pages()[0])
        self.assertNotIn(
            "Phase 99h: protect the default retro header",
            response.content.decode(response.charset),
        )

        self.author.profile.template = "simple_pattern"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(self._public_pages()[0])
        self.assertNotIn(
            "Phase 99h: protect the default retro header",
            response.content.decode(response.charset),
        )
