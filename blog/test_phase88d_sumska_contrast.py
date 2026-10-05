from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Comment, Post


class Phase88dSumskaContrastTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase88d-author")
        cls.reader = User.objects.create_user(username="phase88d-reader")
        cls.post = Post.objects.create(author=cls.author, title="Sumska objava", content="<p>Sadrzaj</p>", status="published")
        Comment.objects.create(post=cls.post, author=cls.reader, content="Komentar")

    def test_blog_and_detail_render_forest_contrast_contract(self):
        self.author.profile.template = "sumska_svjetlost"
        self.author.profile.blog_tagline = "Svjetlo kroz krosnje"
        self.author.profile.save(update_fields=["template", "blog_tagline"])
        for url in (reverse("user_blog", args=[self.author.username]), reverse("post_detail", args=[self.post.pk])):
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                content = response.content.decode(response.charset)
                self.assertIn("Phase 88d", content)
                self.assertIn(".blog-post-entry .blog-rich-content", content)
                self.assertIn(".comment-body .comment-text", content)
                self.assertIn(".archive-link", content)
                self.assertIn("background: #f5fbef !important", content)

    def test_other_design_does_not_receive_forest_contract(self):
        self.author.profile.template = "zlatni_horizont"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn("Phase 88d", response.content.decode(response.charset))
