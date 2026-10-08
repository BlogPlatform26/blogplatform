from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Comment, Post


class Phase97aMjesecevMobilePostLayoutTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase97a-author")
        cls.commenter = User.objects.create_user(username="phase97a-commenter")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Ples pod mjesecevom svjetloscu",
            content="<p>Probni tekst posta.</p>",
            status="published",
        )
        Comment.objects.create(post=cls.post, author=cls.commenter, content="Probni komentar")

    def test_mobile_rules_render_on_blog_and_detail(self):
        self.author.profile.template = "mjesecev_ples"
        self.author.profile.save(update_fields=["template"])

        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                content = response.content.decode(response.charset)
                self.assertIn("Phase 97a: give the post and comments", content)
                self.assertIn("@media (max-width: 575.98px)", content)
                self.assertIn(".blog-post-entry > .d-flex:first-child", content)
                self.assertIn(".comment-item.bp-modern-comment-item", content)

    def test_other_design_does_not_include_mjesecev_mobile_rule(self):
        self.author.profile.template = "default"
        self.author.profile.save(update_fields=["template"])

        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn("Phase 97a: give the post and comments", response.content.decode(response.charset))
