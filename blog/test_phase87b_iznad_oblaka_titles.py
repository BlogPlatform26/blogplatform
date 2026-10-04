from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class Phase87bIznadOblakaTitleTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase87b-author")
        cls.author.profile.blog_tagline = "Tisina iznad svijeta"
        cls.author.profile.save(update_fields=["blog_tagline"])
        cls.post = Post.objects.create(
            author=cls.author,
            title="Let iznad oblaka",
            content="<p>Sadrzaj</p>",
            status="published",
        )

    def test_blog_and_detail_render_photo_independent_title_surfaces(self):
        self.author.profile.template = "iznad_oblaka"
        self.author.profile.save(update_fields=["template"])

        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                content = response.content.decode(response.charset)
                self.assertIn("Phase 87b", content)
                self.assertIn(".blog-header-main .blog-page-title", content)
                self.assertIn(".blog-header-main .blog-page-subtitle", content)
                self.assertIn(".blog-post-entry .blog-post-title", content)
                self.assertIn("background: #514956 !important", content)

    def test_other_design_does_not_receive_cloud_title_surfaces(self):
        self.author.profile.template = "zlatni_horizont"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn("Phase 87b", response.content.decode(response.charset))
