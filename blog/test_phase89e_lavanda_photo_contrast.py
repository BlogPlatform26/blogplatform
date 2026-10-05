from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Comment, Post


class Phase89eLavandaPhotoContrastTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase89e-author")
        cls.reader = User.objects.create_user(username="phase89e-reader")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Lavandin zapis",
            content="<p>Sadrzaj</p>",
            status="published",
        )
        Comment.objects.create(post=cls.post, author=cls.reader, content="Komentar")

    def test_blog_and_detail_render_photo_independent_lavender_contract(self):
        self.author.profile.template = "polje_lavande"
        self.author.profile.save(update_fields=["template"])

        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                content = response.content.decode(response.charset)
                self.assertIn("Phase 89e", content)
                self.assertIn("background: #f5e6fa !important", content)
                self.assertIn("color: #512767 !important", content)
                self.assertIn("--date-primary: #512767", content)

    def test_other_design_does_not_render_lavender_contract(self):
        self.author.profile.template = "zlatno_polje"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn("Phase 89e", response.content.decode(response.charset))
