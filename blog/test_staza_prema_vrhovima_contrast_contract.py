from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Comment, Post


class StazaPremaVrhovimaContrastContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="mountain-contrast-author")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Put prema vrhovima",
            content="<p>Sadrzaj posta</p>",
            status="published",
        )
        Comment.objects.create(
            post=cls.post,
            author=cls.author,
            content="Citljiv komentar",
        )

    def test_blog_and_detail_render_stable_mountain_contrast_surfaces(self):
        self.author.profile.template = "staza_prema_vrhovima"
        self.author.profile.save(update_fields=["template"])

        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                content = response.content.decode(response.charset)
                self.assertIn("Phase 83g: photo-independent", content)
                self.assertIn("background: #2a2119;", content)
                self.assertIn("color: #ffdda5 !important;", content)
                self.assertIn("color: #f5e7d3 !important;", content)
                self.assertIn(".spv-theme .spv-archive-link", content)
                self.assertIn(".spv-theme .calendar-month-nav-link", content)

    def test_other_design_does_not_receive_mountain_contract(self):
        self.author.profile.template = "misticno_jezero"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(
            reverse("user_blog", args=[self.author.username])
        )
        content = response.content.decode(response.charset)
        self.assertNotIn("Phase 83g: photo-independent", content)
