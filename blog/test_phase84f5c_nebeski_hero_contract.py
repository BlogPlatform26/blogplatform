from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class Phase84f5cNebeskiHeroContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase84f5c-author")
        cls.author.profile.blog_tagline = "Mir iznad oblaka"
        cls.author.profile.save(update_fields=["blog_tagline"])
        cls.post = Post.objects.create(
            author=cls.author,
            title="Nebeski hero",
            content="<p>Sadrzaj</p>",
            status="published",
        )

    def test_blog_and_detail_render_nebeski_hero_surface(self):
        self.author.profile.template = "nebeski_mir"
        self.author.profile.save(update_fields=["template"])

        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                content = response.content.decode(response.charset)
                self.assertIn("Phase 84f5c", content)
                self.assertIn("background: #f1f5fb !important", content)
                self.assertIn(
                    "html body .blog-header-main .blog-page-title a", content
                )
                self.assertIn("color: #2f435c !important", content)
                self.assertIn("color: #334155 !important", content)

    def test_other_design_does_not_receive_nebeski_hero_surface(self):
        self.author.profile.template = "planine_u_magli"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn("Phase 84f5c", response.content.decode(response.charset))
