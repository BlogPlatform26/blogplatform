from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Comment, Post


class Phase95c6AsfaltniMobilePostLayoutTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase95c6-author")
        cls.reader = User.objects.create_user(username="phase95c6-reader")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Nocna voznja kroz maglu",
            content="<p>Probni sadrzaj</p>",
            status="published",
        )
        Comment.objects.create(
            post=cls.post,
            author=cls.reader,
            content="Komentar koji ostaje citljiv na uskom zaslonu.",
        )

    def test_mobile_rules_render_on_blog_and_detail(self):
        self.author.profile.template = "asfaltni_plamen"
        self.author.profile.save(update_fields=["template"])
        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                html = response.content.decode(response.charset)
                self.assertIn("Phase 95c6: give the narrow post", html)
                self.assertIn("@media (max-width: 575.98px)", html)
                self.assertIn(".blog-main-content-column .blog-posts-shell", html)
                self.assertIn(".comment-item.bp-modern-comment-item", html)
                self.assertIn(".blog-post-entry .blog-post-title", html)
                self.assertIn("overflow-wrap: anywhere", html)

    def test_other_design_does_not_include_mobile_rule(self):
        self.author.profile.template = "default"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(
            "Phase 95c6: give the narrow post",
            response.content.decode(response.charset),
        )
