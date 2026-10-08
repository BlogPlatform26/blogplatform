from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Comment, Post


class Phase95c4AsfaltniCommentContrastTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase95c4-author")
        cls.author.profile.template = "asfaltni_plamen"
        cls.author.profile.save(update_fields=["template"])
        cls.reader = User.objects.create_user(username="phase95c4-reader")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Probna vožnja",
            content="<p>Probni sadržaj</p>",
            status="published",
        )
        Comment.objects.create(post=cls.post, author=cls.reader, content="Probni komentar")

    def test_comment_ink_and_surface_are_local_to_blog_and_detail(self):
        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            response = self.client.get(url, follow=True)
            self.assertEqual(response.status_code, 200)
            html = response.content.decode(response.charset)
            self.assertIn("Phase 95c4: comments must not inherit", html)
            self.assertIn(".comment-body.bp-modern-comment-body", html)
            self.assertIn("background: #21140e !important", html)
            self.assertIn("color: #e3c7a6 !important", html)
            self.assertIn("opacity: 1 !important", html)

    def test_other_design_does_not_render_asfaltni_comment_rule(self):
        self.author.profile.template = "default"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(
            "Phase 95c4: comments must not inherit",
            response.content.decode(response.charset),
        )
