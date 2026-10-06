from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class Phase92cDimniActionContrastTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase92c-author")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Dimna objava",
            content="<p>Sadržaj</p>",
            status="published",
        )

    def test_blog_and_detail_render_local_action_surfaces(self):
        self.author.profile.template = "dimni_akordi"
        self.author.profile.save(update_fields=["template"])

        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                content = response.content.decode(response.charset)
                self.assertIn("Phase 92c", content)
                self.assertIn('html body [id^="comments-"] > .small.text-muted', content)
                self.assertIn(".post-actions form > button.btn.btn-link", content)
                self.assertIn("background: #21130d !important", content)
                self.assertIn("color: #ffe0be !important", content)

    def test_other_design_does_not_render_smoke_action_contract(self):
        self.author.profile.template = "neonski_grad"
        self.author.profile.save(update_fields=["template"])

        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn("Phase 92c", response.content.decode(response.charset))
