from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Comment, Post


class MagazinContrastContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="magazine-contrast-author")
        cls.author.profile.blog_tagline = "Price izmedu svjetla i sjene"
        cls.author.profile.save(update_fields=["blog_tagline"])
        cls.post = Post.objects.create(
            author=cls.author,
            title="Naslovna prica tjedna",
            content="<p>Sadrzaj posta</p>",
            status="published",
        )
        Comment.objects.create(post=cls.post, author=cls.author, content="Citljiv komentar")

    def test_blog_and_detail_render_stable_magazine_contrast_surfaces(self):
        self.author.profile.template = "magazin"
        self.author.profile.save(update_fields=["template"])
        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                content = response.content.decode(response.charset)
                self.assertIn("Phase 83k: photo-independent", content)
                self.assertIn("background: #2f271f;", content)
                self.assertIn("background: #fffaf5;", content)
                self.assertIn("color: #704414 !important;", content)
                self.assertIn("background: #76583d;", content)

    def test_other_design_does_not_receive_magazine_contract(self):
        self.author.profile.template = "ponocna_elegancija"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn("Phase 83k: photo-independent", response.content.decode(response.charset))
