from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class Phase87cIznadOblakaSidebarContrastTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase87c-author")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Let iznad oblaka",
            content="<p>Sadrzaj</p>",
            status="published",
        )

    def test_blog_and_detail_render_sidebar_contrast_contract(self):
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
                self.assertIn("Phase 87c", content)
                self.assertIn(".calendar-title--nav .calendar-month-nav-link", content)
                self.assertIn(".archive-link", content)
                self.assertIn("color: #514956 !important", content)
                self.assertIn("background: #fff7fc !important", content)

    def test_other_design_does_not_receive_cloud_sidebar_contract(self):
        self.author.profile.template = "zlatni_horizont"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn("Phase 87c", response.content.decode(response.charset))
