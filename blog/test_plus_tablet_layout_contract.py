from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post
from blog.services import set_blog_preferences


class PlusTabletLayoutContractTests(TestCase):
    PLUS_DESIGNS = ("default_right", "dark_right", "classic_right")

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(
            username="plus-tablet-author",
            password="test-password",
        )
        Post.objects.create(
            author=cls.author,
            title="Plus tablet layout post",
            content="<p>Tablet layout content</p>",
            status="published",
        )

    def render_design(self, template_key, right_box_columns):
        self.author.profile.template = template_key
        self.author.profile.save(update_fields=["template"])
        set_blog_preferences(self.author, {
            "design_customizations": {
                template_key: {"right_box_columns": right_box_columns},
            },
        })
        return self.client.get(reverse("user_blog", args=[self.author.username]))

    def test_two_column_plus_designs_render_tablet_stacking_contract(self):
        for template_key in self.PLUS_DESIGNS:
            with self.subTest(template=template_key):
                response = self.render_design(template_key, "2")

                self.assertEqual(response.status_code, 200)
                self.assertContains(
                    response,
                    "BLOGPLATFORM_PLUS_TWO_COLUMN_TABLET_LAYOUT_START",
                )
                self.assertContains(
                    response,
                    "@media (min-width: 768px) and (max-width: 1199.98px)",
                )
                self.assertContains(response, "flex: 0 0 100%;")
                self.assertContains(response, "flex: 0 0 50%;")

    def test_one_column_plus_variant_keeps_existing_layout_branch(self):
        response = self.render_design("default_right", "1")

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(
            response,
            "BLOGPLATFORM_PLUS_TWO_COLUMN_TABLET_LAYOUT_START",
        )
        self.assertContains(response, "flex: 0 0 60%;")
        self.assertContains(response, "flex: 0 0 40%;")

