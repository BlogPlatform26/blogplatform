from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class Phase84f4cPlanineHeroContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase84f4c-author")
        cls.author.profile.blog_tagline = "Magla iznad planina"
        cls.author.profile.save(update_fields=["blog_tagline"])
        cls.post = Post.objects.create(
            author=cls.author,
            title="Planine hero",
            content="<p>Sadrzaj</p>",
            status="published",
        )

    def test_blog_and_detail_render_desktop_planine_hero_surface(self):
        self.author.profile.template = "planine_u_magli"
        self.author.profile.save(update_fields=["template"])

        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                content = response.content.decode(response.charset)
                self.assertIn("Phase 84f4c", content)
                self.assertIn("@media (min-width: 992px)", content)
                self.assertIn("background: #edf1f4 !important", content)
                self.assertIn(
                    "html body .blog-header-main .blog-page-subtitle", content
                )
                self.assertIn("color: #43566c !important", content)

    def test_other_design_does_not_receive_planine_hero_surface(self):
        self.author.profile.template = "nebeski_mir"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn("Phase 84f4c", response.content.decode(response.charset))
