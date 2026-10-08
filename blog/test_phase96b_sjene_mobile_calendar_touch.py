from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class Phase96bSjeneMobileCalendarTouchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase96b-author")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Sjene kalendara",
            content="<p>Sinteticki sadrzaj</p>",
            status="published",
        )

    def test_full_width_mobile_calendar_is_local_to_sjene_blog_and_detail(self):
        self.author.profile.template = "sjene_ulice"
        self.author.profile.save(update_fields=["template"])
        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                html = response.content.decode(response.charset)
                self.assertIn("Phase 96b: give the seven mobile calendar days", html)
                self.assertIn("width: min(100vw, 376px) !important", html)
                self.assertIn("column-gap: 1px", html)
                self.assertIn("min-width: 44px !important", html)

    def test_default_design_does_not_include_sjene_mobile_rule(self):
        self.author.profile.template = "default"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(
            "Phase 96b: give the seven mobile calendar days",
            response.content.decode(response.charset),
        )
