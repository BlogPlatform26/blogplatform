from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class Phase91cKraljevskaTitleContrastTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase91c-author")
        cls.author.profile.template = "kraljevska_pozornica"
        cls.author.profile.blog_tagline = "Tekst preko svjetla"
        cls.author.profile.save(update_fields=["template", "blog_tagline"])
        cls.post = Post.objects.create(
            author=cls.author,
            title="Pozornica",
            content="<p>Sadrzaj</p>",
            status="published",
        )

    def test_blog_and_detail_render_opaque_title_contract(self):
        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            response = self.client.get(url, follow=True)
            self.assertEqual(response.status_code, 200)
            content = response.content.decode(response.charset)
            self.assertIn("Phase 91c: narrow, opaque title cards", content)
            self.assertIn(".blog-header-main .blog-page-subtitle", content)
            self.assertIn("background: #2b0d14 !important", content)
            self.assertIn("color: #fff0d9 !important", content)
            self.assertIn("Tekst preko svjetla", content)
