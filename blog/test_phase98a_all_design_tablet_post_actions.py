from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post, Profile


class AllDesignTabletPostActionsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase98a-author")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Tablet action targets",
            content="<p>Provjera akcija.</p>",
            status="published",
        )

    def test_every_registered_design_renders_shared_tablet_contract(self):
        for template_key, _label in Profile.TEMPLATE_CHOICES:
            self.author.profile.template = template_key
            self.author.profile.save(update_fields=["template"])
            for url in (
                reverse("user_blog", args=[self.author.username]),
                reverse("post_detail", args=[self.post.pk]),
            ):
                with self.subTest(template=template_key, url=url):
                    response = self.client.get(url, follow=True)
                    self.assertEqual(response.status_code, 200)
                    content = response.content.decode(response.charset)
                    self.assertIn("Phase 98a: keep the same action hit areas", content)
                    self.assertIn("@media (min-width: 576px) and (max-width: 991.98px)", content)
                    self.assertIn("html body .post-actions > form > button", content)
                    self.assertIn("html body .post-actions > a", content)
                    self.assertIn("min-height: 44px !important;", content)
