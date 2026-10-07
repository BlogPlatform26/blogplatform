from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class Phase94bMjesecevCalendarGridTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase94b-author")
        cls.author.profile.template = "mjesecev_ples"
        cls.author.profile.save(update_fields=["template"])
        cls.post = Post.objects.create(
            author=cls.author,
            title="Mjesecev ples",
            content="<p>Probni sadržaj</p>",
            status="published",
        )

    def test_mjesecev_calendar_rules_render_on_blog_and_detail(self):
        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            response = self.client.get(url, follow=True)
            self.assertEqual(response.status_code, 200)
            content = response.content.decode(response.charset)
            self.assertIn("Phase 94b: keep the moonlit calendar", content)
            self.assertIn("grid-template-columns: repeat(7, minmax(0, 1fr))", content)
            self.assertIn("(min-width: 768px) and (max-width: 991.98px)", content)
            self.assertIn("min-height: 44px !important", content)

    def test_theme_rule_does_not_render_for_default(self):
        self.author.profile.template = "default"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(
            "Phase 94b: keep the moonlit calendar",
            response.content.decode(response.charset),
        )
