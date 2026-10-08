from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class Phase91fKraljevskaSidebarContrastTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase91f-author")
        cls.author.profile.template = "kraljevska_pozornica"
        cls.author.profile.save(update_fields=["template"])
        cls.post = Post.objects.create(
            author=cls.author,
            title="Probna predstava",
            content="<p>Probni sadržaj</p>",
            status="published",
        )

    def test_sidebar_rules_on_blog_and_detail(self):
        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            response = self.client.get(url, follow=True)
            self.assertEqual(response.status_code, 200)
            html = response.content.decode(response.charset)
            self.assertIn("Phase 91f: stable stage wings", html)
            self.assertIn("html body .calendar-box", html)
            self.assertIn("html body .blog-profile-panel", html)
            self.assertIn("background: rgba(24, 8, 12, 0.90) !important", html)
            self.assertIn("html body .sidebar-box .text-muted", html)

    def test_other_design_does_not_render_kraljevska_sidebar_rules(self):
        self.author.profile.template = "default"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(
            "Phase 91f: stable stage wings",
            response.content.decode(response.charset),
        )
