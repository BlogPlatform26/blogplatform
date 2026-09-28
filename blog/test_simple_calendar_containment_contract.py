from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class SimpleCalendarContainmentContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="simple-calendar-author")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Responsive calendar",
            content="<p>Sadrzaj</p>",
            status="published",
        )

    def test_pattern_and_image_render_responsive_containment(self):
        for template in ("simple_pattern", "simple_image"):
            self.author.profile.template = template
            self.author.profile.save(update_fields=["template"])
            for url in (
                reverse("user_blog", args=[self.author.username]),
                reverse("post_detail", args=[self.post.pk]),
            ):
                with self.subTest(template=template, url=url):
                    response = self.client.get(url, follow=True)
                    self.assertEqual(response.status_code, 200)
                    content = response.content.decode(response.charset)
                    self.assertIn("Phase 84b: contain simple calendar", content)
                    self.assertIn("box-sizing: border-box;", content)
                    self.assertIn("max-width: 100%;", content)

    def test_retro_and_default_do_not_receive_phase84b_rule(self):
        for template in ("simple_retro", "default"):
            self.author.profile.template = template
            self.author.profile.save(update_fields=["template"])
            response = self.client.get(reverse("user_blog", args=[self.author.username]))
            self.assertNotIn(
                "Phase 84b: contain simple calendar",
                response.content.decode(response.charset),
            )
