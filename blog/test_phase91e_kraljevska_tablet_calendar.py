from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class Phase91eKraljevskaTabletCalendarTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase91e-author")
        cls.author.profile.template = "kraljevska_pozornica"
        cls.author.profile.save(update_fields=["template"])
        cls.post = Post.objects.create(
            author=cls.author,
            title="Pozornica",
            content="<p>Sadrzaj</p>",
            status="published",
        )

    def test_local_tablet_calendar_contract_on_blog_and_detail(self):
        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            response = self.client.get(url, follow=True)
            self.assertEqual(response.status_code, 200)
            content = response.content.decode(response.charset)
            self.assertIn("Phase 91e: give the seven-day calendar", content)
            self.assertIn("(min-width: 768px) and (max-width: 991.98px)", content)
            self.assertIn("grid-template-columns: repeat(7, minmax(0, 1fr))", content)
            self.assertIn("min-height: 44px !important", content)

    def test_calendar_rule_does_not_render_for_default_design(self):
        self.author.profile.template = "default"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Phase 91e: give the seven-day calendar", response.content.decode(response.charset))
