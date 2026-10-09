from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post
from blog.services import get_blog_preferences, set_blog_preferences


class FreshSimplePatternHeaderTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Avoid legacy JSON preferences keyed by low user IDs.
        cls.author = User.objects.create_user(id=1001, username="phase100b_author")
        cls.author.profile.template = "simple_pattern"
        cls.author.profile.blog_tagline = "Fresh pattern tagline"
        cls.author.profile.save(update_fields=["template", "blog_tagline"])
        cls.post = Post.objects.create(
            author=cls.author,
            title="Fresh pattern story",
            content="<p>Content</p>",
            status="published",
        )

    def _public_pages(self):
        return (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        )

    def test_factory_orange_gradient_uses_opaque_dark_text(self):
        custom = get_blog_preferences(self.author)["active_design_customization"]
        self.assertEqual(custom["header_background_mode"], "gradient")
        self.assertEqual(custom["header_background_color_1"], "#d98a37")
        self.assertEqual(custom["header_background_color_2"], "#b8641e")
        for url in self._public_pages():
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                html = response.content.decode(response.charset)
                self.assertIn("Phase 100b: protect the fresh default orange pattern header", html)
                self.assertIn("color: #000000 !important", html)
                self.assertIn("opacity: 1", html)

    def test_custom_gradient_and_saved_yellow_palette_are_not_overridden(self):
        set_blog_preferences(self.author, {
            "design_customizations": {
                "simple_pattern": {"header_background_color_1": "#123456"},
            },
        })
        html = self.client.get(self._public_pages()[0]).content.decode()
        self.assertNotIn("Phase 100b: protect the fresh default orange pattern header", html)

        set_blog_preferences(self.author, {
            "design_customizations": {
                "simple_pattern": {
                    "header_background_mode": "color",
                    "header_background_color_1": "#ffd561",
                    "blog_title_color": "#ffffff",
                },
            },
        })
        html = self.client.get(self._public_pages()[0]).content.decode()
        self.assertIn("Phase 99g: keep the default yellow pattern plaque", html)
        self.assertNotIn("Phase 100b: protect the fresh default orange pattern header", html)
