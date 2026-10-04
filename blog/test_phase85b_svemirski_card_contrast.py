from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class Phase85bSvemirskiCardContrastTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase85b-author")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Svemirski zapis",
            content="<p>Sadrzaj</p>",
            status="published",
        )

    def test_blog_and_detail_render_svemirski_contrast_contract(self):
        self.author.profile.template = "svemirski_horizont"
        self.author.profile.save(update_fields=["template"])

        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                content = response.content.decode(response.charset)
                self.assertIn("Phase 85b", content)
                self.assertIn(".post-actions button.btn-link", content)
                self.assertIn('[id^="comments-"] .small.text-muted', content)
                self.assertIn(
                    ".calendar-title--nav .calendar-month-nav-link", content
                )
                self.assertIn("background: rgba(4, 12, 28, 0.72) !important", content)

    def test_other_design_does_not_receive_svemirski_contract(self):
        self.author.profile.template = "zlatni_horizont"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn("Phase 85b", response.content.decode(response.charset))
