from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class Phase90bCarobnaActionsContrastTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase90b-author")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Ljubičasta objava",
            content="<p>Sadržaj</p>",
            status="published",
        )

    def test_blog_and_detail_render_local_action_surfaces(self):
        self.author.profile.template = "carobna_ljubicasta"
        self.author.profile.save(update_fields=["template"])

        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                content = response.content.decode(response.charset)
                self.assertIn("Phase 90b", content)
                self.assertIn('html body [id^="comments-"] > .small.text-muted', content)
                self.assertIn(".post-actions form > button.btn.btn-link", content)
                self.assertIn("background: #211038 !important", content)
                self.assertIn("color: #f6c7ff !important", content)

    def test_other_design_does_not_render_violet_action_contract(self):
        self.author.profile.template = "neonski_grad"
        self.author.profile.save(update_fields=["template"])

        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn("Phase 90b", response.content.decode(response.charset))
