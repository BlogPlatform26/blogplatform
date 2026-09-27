from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Comment, Post


class StaraAlejaContrastContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="stara-contrast-author")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Naslov kroz aleju",
            content="<p>Sadrzaj posta</p>",
            status="published",
        )
        Comment.objects.create(
            post=cls.post,
            author=cls.author,
            content="Citljiv komentar",
        )

    def test_blog_and_detail_render_photo_independent_contrast_surfaces(self):
        self.author.profile.template = "stara_aleja"
        self.author.profile.save(update_fields=["template"])

        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                content = response.content.decode(response.charset)
                self.assertIn("background: #fbf3e7;", content)
                self.assertIn("background: #251d18 !important;", content)
                self.assertIn(".sa-post .post-author-link a", content)
                self.assertIn(".comment-body .comment-author a", content)
                self.assertIn("color: #ffe0b4 !important;", content)

    def test_mobile_comment_exception_remains_in_shared_component(self):
        self.author.profile.template = "stara_aleja"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(
            reverse("user_blog", args=[self.author.username])
        )
        content = response.content.decode(response.charset)
        self.assertIn("@media (max-width: 576px)", content)
        self.assertIn("--bp-mobile-comment-surface: #251d18", content)

    def test_other_design_does_not_receive_stara_aleja_contract(self):
        self.author.profile.template = "misticno_jezero"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(
            reverse("user_blog", args=[self.author.username])
        )
        content = response.content.decode(response.charset)
        self.assertNotIn(".sa-post .post-author-link a", content)
