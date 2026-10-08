from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post, Profile


class BlogTitleWrapTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase98b-author")
        cls.author.profile.blog_name = "NePrekinutiNaslovBlogaZaProvjeruMobilneSirine1234567890"
        cls.author.profile.save(update_fields=["blog_name"])
        cls.post = Post.objects.create(
            author=cls.author,
            title="Provjera naslova bloga",
            content="<p>Probni tekst.</p>",
            status="published",
        )

    def test_all_designs_render_shared_title_containment_on_blog_and_detail(self):
        for key, _label in Profile.TEMPLATE_CHOICES:
            self.author.profile.template = key
            self.author.profile.save(update_fields=["template"])
            for url in (
                reverse("user_blog", args=[self.author.username]),
                reverse("post_detail", args=[self.post.pk]),
            ):
                with self.subTest(design=key, url=url):
                    response = self.client.get(url, follow=True)
                    self.assertEqual(response.status_code, 200)
                    content = response.content.decode(response.charset)
                    self.assertIn("Phase 98b: break only unspaced blog names", content)
                    self.assertIn("html body .blog-page-title {", content)
                    self.assertIn("overflow-wrap: anywhere;", content)
                    self.assertIn(self.author.profile.blog_name, content)
