from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Comment, Post


class Phase88c2PolarnaCommentArchiveContrastTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase88c2-author")
        cls.reader = User.objects.create_user(username="phase88c2-reader")
        cls.post = Post.objects.create(author=cls.author, title="Polarna objava", content="<p>Sadrzaj</p>", status="published")
        Comment.objects.create(post=cls.post, author=cls.reader, content="Komentar")

    def test_blog_and_detail_render_comment_archive_contrast_contract(self):
        self.author.profile.template = "polarna_svjetlost"
        self.author.profile.save(update_fields=["template"])
        for url in (reverse("user_blog", args=[self.author.username]), reverse("post_detail", args=[self.post.pk])):
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                content = response.content.decode(response.charset)
                self.assertIn("Phase 88c2", content)
                self.assertIn(".comment-body .comment-text", content)
                self.assertIn(".comment-body .comment-author a", content)
                self.assertIn(".archive-link", content)
                self.assertIn("background: #f1fbff !important", content)

    def test_other_design_does_not_receive_polar_comment_archive_contract(self):
        self.author.profile.template = "zlatni_horizont"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn("Phase 88c2", response.content.decode(response.charset))
