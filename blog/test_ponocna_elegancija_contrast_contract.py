from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Comment, Post


class PonocnaElegancijaContrastContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="midnight-contrast-author")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Zapisi poslije ponoci",
            content="<p>Sadrzaj posta</p>",
            status="published",
        )
        Comment.objects.create(post=cls.post, author=cls.author, content="Citljiv komentar")

    def test_blog_and_detail_render_stable_midnight_contrast_surfaces(self):
        self.author.profile.template = "ponocna_elegancija"
        self.author.profile.save(update_fields=["template"])
        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                content = response.content.decode(response.charset)
                self.assertIn("Phase 83j: photo-independent", content)
                self.assertIn("background: #090f1c;", content)
                self.assertIn("color: #f0dfb1 !important;", content)
                self.assertIn("color: #dce1ee !important;", content)
                self.assertIn(".pe-theme .pe-archive-link", content)

    def test_other_design_does_not_receive_midnight_contract(self):
        self.author.profile.template = "nebeska_klasika"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn("Phase 83j: photo-independent", response.content.decode(response.charset))
