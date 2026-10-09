from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post
from blog.services import set_blog_preferences


class SimpleImageHeaderContrastTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase99e_author")
        cls.author.profile.template = "simple_image"
        cls.author.profile.blog_tagline = "A reading room"
        cls.author.profile.save(update_fields=["template", "blog_tagline"])
        cls.post = Post.objects.create(
            author=cls.author,
            title="Header contrast",
            content="<p>Content</p>",
            status="published",
        )

    def _public_pages(self):
        return (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        )

    def test_default_gold_header_has_readable_title_and_tagline(self):
        for url in self._public_pages():
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                html = response.content.decode(response.charset)
                self.assertIn("Phase 99e: preserve the default gold plaque", html)
                self.assertIn("color: #3f3128 !important", html)
                self.assertIn("opacity: 1", html)

    def test_custom_header_and_other_template_keep_their_own_palette(self):
        set_blog_preferences(self.author, {
            "design_customizations": {
                "simple_image": {"header_background_color_1": "#123456"},
            },
        })
        response = self.client.get(self._public_pages()[0])
        self.assertNotIn(
            "Phase 99e: preserve the default gold plaque",
            response.content.decode(response.charset),
        )

        self.author.profile.template = "simple_pattern"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(self._public_pages()[0])
        self.assertNotIn(
            "Phase 99e: preserve the default gold plaque",
            response.content.decode(response.charset),
        )
