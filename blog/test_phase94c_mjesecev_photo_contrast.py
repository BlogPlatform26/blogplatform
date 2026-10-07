from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Comment, Post


class Phase94cMjesecevPhotoContrastTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase94c-author")
        cls.author.profile.template = "mjesecev_ples"
        cls.author.profile.save(update_fields=["template"])
        cls.commenter = User.objects.create_user(username="phase94c-commenter")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Mjesecev ples",
            content="<p>Probni sadržaj</p>",
            status="published",
        )
        Comment.objects.create(
            post=cls.post,
            author=cls.commenter,
            content="Probni komentar",
        )

    def test_mjesecev_opaque_surfaces_render_on_blog_and_detail(self):
        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            response = self.client.get(url, follow=True)
            self.assertEqual(response.status_code, 200)
            content = response.content.decode(response.charset)
            self.assertIn("Phase 94c: keep moonlit foreground readable", content)
            self.assertIn("html body .blog-header-main .blog-page-title", content)
            self.assertIn("html body .blog-profile-panel", content)
            self.assertIn(".comment-body.bp-modern-comment-body", content)
            self.assertIn("html body .post-actions form > button.btn.btn-link", content)
            self.assertIn("background: #241b18 !important", content)

    def test_theme_rules_do_not_render_for_default(self):
        self.author.profile.template = "default"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(
            "Phase 94c: keep moonlit foreground readable",
            response.content.decode(response.charset),
        )
