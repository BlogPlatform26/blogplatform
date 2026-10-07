from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class Phase93dSjenePhotoContrastTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase93d-author")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Sjene ulice",
            content="<p>Probni sadržaj</p>",
            status="published",
        )

    def test_blog_and_detail_render_local_opaque_surfaces(self):
        self.author.profile.template = "sjene_ulice"
        self.author.profile.save(update_fields=["template"])

        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                content = response.content.decode(response.charset)
                self.assertIn("Phase 93d", content)
                self.assertIn("html body .blog-header-main .blog-page-title", content)
                self.assertIn("html body .blog-post-entry", content)
                self.assertIn("html body .blog-profile-panel", content)
                self.assertIn("background: #241813 !important", content)

    def test_other_design_omits_sjene_photo_surfaces(self):
        self.author.profile.template = "default"
        self.author.profile.save(update_fields=["template"])

        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn("Phase 93d", response.content.decode(response.charset))
