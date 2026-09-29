from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class Phase84f2CommentContrastContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase84f2-author")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Comment contrast",
            content="<p>Sadrzaj</p>",
            status="published",
        )

    def test_litica_and_podvodna_render_local_hint_contract(self):
        for template in ("litica_noci", "podvodna_tisina"):
            self.author.profile.template = template
            self.author.profile.save(update_fields=["template"])
            response = self.client.get(reverse("user_blog", args=[self.author.username]))
            self.assertEqual(response.status_code, 200)
            content = response.content.decode(response.charset)
            self.assertIn("Phase 84f2", content)
            self.assertIn('[id^="comments-"] > .small.text-muted', content)
            self.assertIn("#b8c9e5", content)

    def test_podvodna_renders_desktop_author_override_only(self):
        self.author.profile.template = "podvodna_tisina"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("post_detail", args=[self.post.pk]), follow=True)
        content = response.content.decode(response.charset)
        self.assertIn("@media (min-width: 768px)", content)
        self.assertIn("color: #d5e5ff !important", content)

        self.author.profile.template = "litica_noci"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("post_detail", args=[self.post.pk]), follow=True)
        self.assertNotIn("color: #d5e5ff !important", response.content.decode(response.charset))

    def test_unrelated_design_does_not_render_phase84f2_contract(self):
        self.author.profile.template = "default"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn("Phase 84f2", response.content.decode(response.charset))
