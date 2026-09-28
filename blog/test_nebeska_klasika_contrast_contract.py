from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Comment, Post


class NebeskaKlasikaContrastContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="celestial-contrast-author")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Ispod nebeskog svoda",
            content="<p>Sadrzaj posta</p>",
            status="published",
        )
        Comment.objects.create(post=cls.post, author=cls.author, content="Citljiv komentar")

    def test_blog_and_detail_render_stable_celestial_contrast_surfaces(self):
        self.author.profile.template = "nebeska_klasika"
        self.author.profile.save(update_fields=["template"])
        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                content = response.content.decode(response.charset)
                self.assertIn("Phase 83i: photo-independent", content)
                self.assertIn("background: #f8f5ee;", content)
                self.assertIn("color: #455675 !important;", content)
                self.assertIn("background: #536789;", content)
                self.assertIn(".nk-theme .nk-archive-link", content)

    def test_other_design_does_not_receive_celestial_contract(self):
        self.author.profile.template = "misticno_jezero"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn("Phase 83i: photo-independent", response.content.decode(response.charset))
