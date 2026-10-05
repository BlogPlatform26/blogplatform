from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class Phase89bNeonskiGuestHintContrastTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase89b-author")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Neonska objava",
            content="<p>Sadrzaj</p>",
            status="published",
        )

    def test_blog_and_detail_render_neon_guest_hint_contract(self):
        self.author.profile.template = "neonski_grad"
        self.author.profile.save(update_fields=["template"])

        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                content = response.content.decode(response.charset)
                self.assertIn("Phase 89b", content)
                self.assertIn('[id^="comments-"] > .small.text-muted', content)
                self.assertIn("background: #0b081d !important", content)
                self.assertIn("color: #f0e4ff !important", content)

    def test_other_design_does_not_render_neon_guest_hint_contract(self):
        self.author.profile.template = "zlatno_polje"
        self.author.profile.save(update_fields=["template"])

        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn("Phase 89b", response.content.decode(response.charset))
