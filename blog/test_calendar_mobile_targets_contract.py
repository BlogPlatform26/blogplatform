from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post, Profile
from blog.services import set_blog_preferences


class CalendarMobileTargetsContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(
            username="calendar-target-author",
            password="test-password",
        )
        cls.post = Post.objects.create(
            author=cls.author,
            title="Calendar target post",
            content="<p>Calendar target content</p>",
            status="published",
        )
        set_blog_preferences(cls.author, {"blog_archive_mode": "both"})

    def test_every_registered_design_uses_shared_mobile_target_contract(self):
        url = reverse("user_blog", args=[self.author.username])

        for template_key, _label in Profile.TEMPLATE_CHOICES:
            with self.subTest(template=template_key):
                self.author.profile.template = template_key
                self.author.profile.save(update_fields=["template"])

                response = self.client.get(url)
                content = response.content.decode()

                self.assertEqual(response.status_code, 200)
                self.assertIn("BLOGPLATFORM_MOBILE_CALENDAR_TARGETS_START", content)
                self.assertIn("html body .calendar-month-nav-link", content)
                self.assertIn('html body a[class*="calendar-day"]', content)
                self.assertIn('html body a[class*="archive-link"]', content)
                self.assertIn("min-width: 44px !important;", content)
                self.assertIn("min-height: 44px !important;", content)
                self.assertRegex(content, r'class="[^"]*calendar-month-nav-link')
                self.assertRegex(content, r'<a[^>]+class="[^"]*calendar-day')
                self.assertRegex(content, r'<a[^>]+class="[^"]*archive-link')
