from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class SharedBaseTabletPostActionsContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="tablet-actions-author")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Tablet actions",
            content="<p>Sadrzaj</p>",
            status="published",
        )

    def test_nine_shared_base_designs_render_tablet_target_contract(self):
        templates = (
            "default",
            "dark",
            "classic",
            "default_right",
            "dark_right",
            "classic_right",
            "simple_pattern",
            "simple_image",
            "simple_retro",
        )
        for template in templates:
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
                    self.assertIn("Phase 84e: preserve 44px post-action", content)
                    self.assertIn("min-width: 576px", content)
                    self.assertIn("max-width: 991.98px", content)

    def test_bespoke_design_does_not_render_phase84e_contract(self):
        self.author.profile.template = "nebesko_polje"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn(
            "Phase 84e: preserve 44px post-action",
            response.content.decode(response.charset),
        )
