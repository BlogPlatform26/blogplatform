from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class SharedAuthorLinkContrastContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase99b_author")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Post for author link contrast",
            content="<p>Content</p>",
            status="published",
        )

    def test_six_base_variants_include_author_opacity_contract(self):
        for template in (
            "default", "dark", "classic",
            "default_right", "dark_right", "classic_right",
        ):
            self.author.profile.template = template
            self.author.profile.save(update_fields=["template"])
            for url in (
                reverse("user_blog", args=[self.author.username]),
                reverse("post_detail", args=[self.post.pk]),
            ):
                with self.subTest(template=template, url=url):
                    response = self.client.get(url, follow=True)
                    self.assertEqual(response.status_code, 200)
                    self.assertIn(
                        "Phase 99b: keep the author link's theme color",
                        response.content.decode(response.charset),
                    )

    def test_simple_variants_do_not_inherit_author_opacity_contract(self):
        for template in ("simple_pattern", "simple_image", "simple_retro"):
            self.author.profile.template = template
            self.author.profile.save(update_fields=["template"])
            response = self.client.get(reverse("user_blog", args=[self.author.username]))
            self.assertNotIn(
                "Phase 99b: keep the author link's theme color",
                response.content.decode(response.charset),
            )
