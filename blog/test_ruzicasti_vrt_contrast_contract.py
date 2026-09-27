from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Comment, Post


class RuzicastiVrtContrastContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="rose-contrast-author")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Ruze kroz fotografiju",
            content="<p>Sadrzaj posta</p>",
            status="published",
        )
        Comment.objects.create(
            post=cls.post,
            author=cls.author,
            content="Citljiv komentar",
        )

    def test_blog_and_detail_render_stable_rose_contrast_surfaces(self):
        self.author.profile.template = "ruzicasti_vrt"
        self.author.profile.save(update_fields=["template"])

        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                content = response.content.decode(response.charset)
                self.assertIn("Phase 83d: photo-independent", content)
                self.assertIn("background: #fff1f4;", content)
                self.assertIn("color: #6f2945 !important;", content)
                self.assertIn("color: #7a2847 !important;", content)
                self.assertIn(".rv-theme .rv-archive-link", content)
                self.assertIn(".rv-theme .calendar-month-nav-link", content)

    def test_other_design_does_not_receive_rose_contract(self):
        self.author.profile.template = "ponocna_elegancija"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(
            reverse("user_blog", args=[self.author.username])
        )
        content = response.content.decode(response.charset)
        self.assertNotIn("Phase 83d: photo-independent", content)
