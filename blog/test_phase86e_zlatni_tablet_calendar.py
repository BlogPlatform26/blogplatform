from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class Phase86eZlatniTabletCalendarTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase86e-author")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Zlatni zapis",
            content="<p>Sadrzaj</p>",
            status="published",
        )

    def test_blog_and_detail_render_tablet_calendar_contract(self):
        self.author.profile.template = "zlatni_horizont"
        self.author.profile.save(update_fields=["template"])

        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                content = response.content.decode(response.charset)
                self.assertIn("Phase 86e", content)
                self.assertIn("@media (min-width: 768px) and (max-width: 991.98px)", content)
                self.assertIn("repeat(7, minmax(44px, 1fr))", content)
                self.assertIn("gap: 0", content)
                self.assertIn("min-width: 44px", content)
                self.assertIn("min-height: 44px", content)
                self.assertIn("transform: translateY(-1px)", content)

    def test_other_design_does_not_receive_zlatni_tablet_calendar_contract(self):
        self.author.profile.template = "iznad_oblaka"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn("Phase 86e", response.content.decode(response.charset))
