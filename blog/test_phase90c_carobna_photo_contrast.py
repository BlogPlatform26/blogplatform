from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class Phase90cCarobnaPhotoContrastTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase90c-author")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Ljubičasta objava",
            content="<p>Sadržaj</p>",
            status="published",
        )

    def test_blog_and_detail_render_local_photo_contrast_contract(self):
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
                self.assertIn("Phase 90c", content)
                self.assertIn(".blog-header-main .blog-page-subtitle", content)
                self.assertIn("html body .blog-post-entry", content)
                self.assertIn(".comment-body.bp-modern-comment-body", content)
                self.assertIn("background: rgba(33, 12, 56, 0.84) !important", content)
                self.assertIn("background: rgba(33, 12, 56, 0.90) !important", content)

    def test_other_design_omits_violet_photo_contract(self):
        self.author.profile.template = "neonski_grad"
        self.author.profile.save(update_fields=["template"])

        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn("Phase 90c", response.content.decode(response.charset))
