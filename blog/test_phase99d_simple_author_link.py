from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class SimpleAuthorLinkContrastContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase99d_author")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Simple author link",
            content="<p>Content</p>",
            status="published",
        )

    def test_simple_variants_style_actual_author_anchor(self):
        for template in ("simple_pattern", "simple_image", "simple_retro"):
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
                    self.assertIn(
                        "Phase 99d: color the actual author anchor",
                        content,
                    )
                    if template == "simple_retro":
                        self.assertIn(
                            ".blog-posts-shell--simple-retro .post-author-link a",
                            content,
                        )

    def test_default_does_not_inherit_simple_author_rule(self):
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn(
            "Phase 99d: color the actual author anchor",
            response.content.decode(response.charset),
        )
