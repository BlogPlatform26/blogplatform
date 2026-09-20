from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class DirectPostMobileTouchContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(username="touch-owner", password="test-password")
        cls.post = Post.objects.create(
            author=cls.owner, title="Touch draft", content="<p>Text</p>", status="draft"
        )

    def test_forms_have_scoped_mobile_touch_rules(self):
        self.client.force_login(self.owner)
        create = self.client.get(reverse("create_post"))
        edit = self.client.get(reverse("edit_post", args=[self.post.pk]))
        self.assertContains(create, 'id="createPostForm"')
        self.assertContains(edit, 'id="editPostForm"')

        css = (
            Path(settings.BASE_DIR) / "blog" / "static" / "blog" / "css" / "ckeditor5-custom.css"
        ).read_text(encoding="utf-8")
        self.assertIn("@media (max-width: 575.98px)", css)
        for selector in (
            "#createPostForm .ck-toolbar .ck-button",
            "#editPostForm .ck-toolbar .ck-button",
            "#editPostForm .edit-post-options-inner",
            "#createPostForm > button[type=\"submit\"]",
            "#editPostForm .edit-post-actions .btn",
        ):
            self.assertIn(selector, css)
        self.assertIn("min-height: 44px !important;", css)
        self.assertIn("min-width: 44px !important;", css)
