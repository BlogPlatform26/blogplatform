from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post, Profile


class MobilePostActionTargetsContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="post-action-target-author")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Mobile post action targets",
            content="<p>Target contract</p>",
            status="published",
        )

    def test_every_registered_design_receives_shared_mobile_action_contract(self):
        url = reverse("user_blog", args=[self.author.username])

        for template_key, _label in Profile.TEMPLATE_CHOICES:
            with self.subTest(template=template_key):
                self.author.profile.template = template_key
                self.author.profile.save(update_fields=["template"])
                response = self.client.get(url)
                content = response.content.decode(response.charset)

                self.assertEqual(response.status_code, 200)
                self.assertIn("BLOGPLATFORM_MOBILE_POST_ACTION_TARGETS_START", content)
                self.assertIn("@media (max-width: 575.98px)", content)
                self.assertIn("html body .post-actions > form > button", content)
                self.assertIn("html body .post-actions > a", content)
                self.assertIn("min-height: 44px !important;", content)

    def test_detail_route_uses_same_shared_action_markup(self):
        response = self.client.get(
            reverse("post_detail", args=[self.post.pk]), follow=True
        )
        content = response.content.decode(response.charset)
        self.assertEqual(response.status_code, 200)
        self.assertIn("BLOGPLATFORM_MOBILE_POST_ACTION_TARGETS_START", content)
        self.assertIn('class="text-decoration-none js-scroll-to-comments"', content)
