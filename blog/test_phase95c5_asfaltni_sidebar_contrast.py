from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class Phase95c5AsfaltniSidebarContrastTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase95c5-author")
        cls.author.profile.template = "asfaltni_plamen"
        cls.author.profile.save(update_fields=["template"])
        cls.post = Post.objects.create(
            author=cls.author,
            title="Probna vožnja",
            content="<p>Probni sadržaj</p>",
            status="published",
        )

    def test_sidebar_backing_is_local_to_asfaltni_blog_and_detail(self):
        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            response = self.client.get(url, follow=True)
            self.assertEqual(response.status_code, 200)
            html = response.content.decode(response.charset)
            self.assertIn("Phase 95c5: readable sidebar surfaces", html)
            for selector in (
                "html body .calendar-box",
                "html body .archive-box",
                "html body .sidebar-box",
                "html body .blog-profile-panel",
            ):
                self.assertIn(selector, html)
            self.assertIn("background: rgba(24, 17, 13, 0.85) !important", html)

    def test_other_design_is_unchanged(self):
        self.author.profile.template = "default"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(
            "Phase 95c5: readable sidebar surfaces",
            response.content.decode(response.charset),
        )
