from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class DefaultCalendarPostTodayContrastTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase99c_author")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Post on today",
            content="<p>Content</p>",
            status="published",
        )

    def test_default_variants_keep_today_post_day_opaque(self):
        for template in ("default", "default_right"):
            self.author.profile.template = template
            self.author.profile.save(update_fields=["template"])
            for url in (
                reverse("user_blog", args=[self.author.username]),
                reverse("post_detail", args=[self.post.pk]),
            ):
                with self.subTest(template=template, url=url):
                    response = self.client.get(url, follow=True)
                    self.assertEqual(response.status_code, 200)
                    self.assertIn(
                        "Phase 99c: the pale post-day gradient",
                        response.content.decode(response.charset),
                    )

    def test_classic_does_not_inherit_default_calendar_rule(self):
        self.author.profile.template = "classic"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn(
            "Phase 99c: the pale post-day gradient",
            response.content.decode(response.charset),
        )
