from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class Phase85cSvemirskiTitleContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase85c-author")
        cls.author.profile.blog_tagline = "Izmedju zvijezda"
        cls.author.profile.save(update_fields=["blog_tagline"])
        cls.post = Post.objects.create(
            author=cls.author,
            title="Svemirski zapis",
            content="<p>Sadrzaj</p>",
            status="published",
        )

    def test_blog_and_detail_render_title_surface_only(self):
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
                self.assertIn("Phase 85c", content)
                self.assertIn("html body .blog-page-title a", content)
                self.assertIn("background: #081326 !important", content)
                self.assertIn("box-decoration-break: clone", content)
                self.assertIn("text-shadow: none !important", content)

    def test_other_design_does_not_receive_svemirski_title_surface(self):
        self.author.profile.template = "zlatni_horizont"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn("Phase 85c", response.content.decode(response.charset))
