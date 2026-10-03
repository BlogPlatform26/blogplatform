from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Comment, Post


class Phase84f3bVodopadContrastContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase84f3b-author")
        cls.reader = User.objects.create_user(username="phase84f3b-reader")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Vodopad contrast",
            content="<p>Sadrzaj</p>",
            status="published",
        )
        Comment.objects.create(
            post=cls.post,
            author=cls.reader,
            content="Citljiv komentar",
        )

    def test_blog_and_detail_render_vodopad_contrast_contract(self):
        self.author.profile.template = "vodopad_u_magli"
        self.author.profile.blog_tagline = "Tagline preko fotografije"
        self.author.profile.save(update_fields=["template", "blog_tagline"])

        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                content = response.content.decode(response.charset)
                self.assertIn("Phase 84f3b", content)
                self.assertIn(".post-author-link a,", content)
                self.assertIn(".post-actions button,", content)
                self.assertIn("color: #43513e !important", content)
                self.assertIn("color: #465042 !important", content)
                self.assertIn("background: #eef0e9 !important", content)
                self.assertIn("@media (min-width: 992px)", content)

    def test_other_design_does_not_receive_vodopad_contract(self):
        self.author.profile.template = "planine_u_magli"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn("Phase 84f3b", response.content.decode(response.charset))
