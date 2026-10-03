from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Comment, Post


class Phase84f5bNebeskiCardContrastContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase84f5b-author")
        cls.reader = User.objects.create_user(username="phase84f5b-reader")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Nebeski contrast",
            content="<p>Sadrzaj</p>",
            status="published",
        )
        Comment.objects.create(
            post=cls.post,
            author=cls.reader,
            content="Citljiv komentar",
        )

    def test_blog_and_detail_render_nebeski_card_contrast_contract(self):
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
                self.assertIn("Phase 84f5b", content)
                self.assertIn(".post-author-link a,", content)
                self.assertIn(".post-actions button,", content)
                self.assertIn(".calendar-month-nav-link", content)
                self.assertIn("color: #315f8d !important", content)
                self.assertIn("color: #334155 !important", content)

    def test_other_design_does_not_receive_nebeski_card_contract(self):
        self.author.profile.template = "planine_u_magli"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn("Phase 84f5b", response.content.decode(response.charset))
