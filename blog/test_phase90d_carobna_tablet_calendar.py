from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class Phase90dCarobnaTabletCalendarTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase90d-author")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Kalendarska objava",
            content="<p>Sadržaj</p>",
            status="published",
        )

    def test_blog_and_detail_render_local_tablet_calendar_contract(self):
        self.author.profile.template = "carobna_ljubicasta"
        self.author.profile.save(update_fields=["template"])

        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                content = response.content.decode(response.charset)
                self.assertIn("Phase 90d", content)
                self.assertIn("@media (min-width: 768px) and (max-width: 991.98px)", content)
                self.assertIn(".blog-main-layout-row > .blog-main-content-column", content)
                self.assertIn("grid-template-columns: repeat(7, minmax(0, 1fr)) !important", content)
                self.assertIn("min-width: 44px !important", content)
                self.assertIn("min-height: 44px !important", content)

    def test_other_design_omits_violet_tablet_calendar_contract(self):
        self.author.profile.template = "neonski_grad"
        self.author.profile.save(update_fields=["template"])

        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn("Phase 90d", response.content.decode(response.charset))
