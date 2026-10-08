from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class Phase96cMjesecevMobileCalendarTouchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase96c-author")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Mjesecev kalendar",
            content="<p>Sinteticki sadrzaj</p>",
            status="published",
        )

    def test_mobile_calendar_rule_is_local_to_mjesecev_blog_and_detail(self):
        self.author.profile.template = "mjesecev_ples"
        self.author.profile.save(update_fields=["template"])
        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                html = response.content.decode(response.charset)
                self.assertIn("Phase 96c: let all seven moonlit day targets", html)
                self.assertIn("width: min(100vw, 376px) !important", html)
                self.assertIn("column-gap: 1px !important", html)
                self.assertIn("min-width: 44px !important", html)

    def test_default_design_does_not_include_mjesecev_rule(self):
        self.author.profile.template = "default"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(
            "Phase 96c: let all seven moonlit day targets",
            response.content.decode(response.charset),
        )
