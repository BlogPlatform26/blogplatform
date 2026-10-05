from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class Phase88bPolarnaActionsContrastTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase88b-author")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Polarna objava",
            content="<p>Sadrzaj</p>",
            status="published",
        )

    def test_blog_and_detail_render_action_contrast_contract(self):
        self.author.profile.template = "polarna_svjetlost"
        self.author.profile.save(update_fields=["template"])
        for url in (reverse("user_blog", args=[self.author.username]), reverse("post_detail", args=[self.post.pk])):
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                content = response.content.decode(response.charset)
                self.assertIn("Phase 88b", content)
                self.assertIn(".blog-post-entry .post-actions button", content)
                self.assertIn(".blog-post-entry .post-actions .post-views", content)
                self.assertIn("color: #123047 !important", content)
                self.assertIn("background: #f1fbff !important", content)

    def test_other_design_does_not_receive_polar_action_contract(self):
        self.author.profile.template = "zlatni_horizont"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn("Phase 88b", response.content.decode(response.charset))
