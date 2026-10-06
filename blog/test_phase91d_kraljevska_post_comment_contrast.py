from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Comment, Post


class Phase91dKraljevskaPostCommentContrastTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase91d-author")
        cls.author.profile.template = "kraljevska_pozornica"
        cls.author.profile.save(update_fields=["template"])
        cls.post = Post.objects.create(
            author=cls.author,
            title="Pozornica",
            content="<p>Sadrzaj</p>",
            status="published",
        )
        Comment.objects.create(post=cls.post, author=cls.author, content="Komentar")

    def test_blog_and_detail_render_opaque_post_comment_contract(self):
        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            response = self.client.get(url, follow=True)
            self.assertEqual(response.status_code, 200)
            content = response.content.decode(response.charset)
            self.assertIn("Phase 91d: keep the post", content)
            self.assertIn("background: #2b0d14 !important", content)
            self.assertIn("background: #3a1c23 !important", content)
            self.assertIn("color: #f4ddd1 !important", content)
            self.assertIn("color: #ffcf9f !important", content)
            self.assertIn("Komentar", content)
