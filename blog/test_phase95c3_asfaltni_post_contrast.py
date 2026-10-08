from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class Phase95c3AsfaltniPostContrastTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase95c3-author")
        cls.author.profile.template = "asfaltni_plamen"
        cls.author.profile.save(update_fields=["template"])
        cls.post = Post.objects.create(
            author=cls.author,
            title="Probna vožnja",
            content="<p>Probni sadržaj</p>",
            status="published",
        )

    def test_post_backing_is_local_to_asfaltni_blog_and_detail(self):
        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            response = self.client.get(url, follow=True)
            self.assertEqual(response.status_code, 200)
            html = response.content.decode(response.charset)
            self.assertIn("Phase 95c3: post copy and links", html)
            self.assertIn("html body .blog-post-entry", html)
            self.assertIn("background: rgba(24, 17, 13, 0.85) !important", html)

    def test_other_design_is_unchanged(self):
        self.author.profile.template = "default"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Phase 95c3: post copy and links", response.content.decode(response.charset))
