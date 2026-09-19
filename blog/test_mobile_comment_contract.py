from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Comment, Post


class MobileCommentContractTests(TestCase):
    CONTRAST_SURFACES = {
        "jedro_u_suton": "#fff7e9",
        "stara_aleja": "#251d18",
        "nebeski_mir": "#f9fbff",
        "sumska_svjetlost": "#f6f8f1",
        "polarna_svjetlost": "#101c2f",
        "zlatno_polje": "#fff6df",
    }

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(
            username="mobile-comment-author", password="test-password"
        )
        cls.post = Post.objects.create(
            author=cls.author,
            title="Mobile comment contract",
            content="<p>Post body</p>",
            status="published",
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.author,
            content="A readable mobile comment",
        )

    def test_shared_component_exposes_edit_action_in_three_design_families(self):
        self.client.force_login(self.author)
        url = reverse("user_blog", args=[self.author.username])

        for template in ("default", "dark", "ponocna_elegancija"):
            with self.subTest(template=template):
                self.author.profile.template = template
                self.author.profile.save(update_fields=["template"])
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                content = response.content.decode(response.charset)
                self.assertIn(f'data-edit-comment-toggle="{self.comment.pk}"', content)
                self.assertIn(f'data-edit-comment-form="{self.comment.pk}"', content)
                self.assertIn("@media (hover: none), (max-width: 576px)", content)
                self.assertIn("visibility: visible !important;", content)
                self.assertIn("pointer-events: auto !important;", content)
                self.assertIn("min-width: 44px !important;", content)
                self.assertIn("font-size: 16px !important;", content)

    def test_static_comment_text_uses_readable_mobile_size(self):
        css = (
            Path(settings.BASE_DIR) / "blog/static/blog/css/comment_text_fix.css"
        ).read_text(encoding="utf-8")
        self.assertIn("@media (max-width: 576px)", css)
        self.assertIn("font-size: 16px !important;", css)
        self.assertIn("font-size: 12px !important;", css)

    def test_risky_designs_render_their_own_mobile_comment_surfaces(self):
        url = reverse("user_blog", args=[self.author.username])
        detail_url = reverse("post_detail", args=[self.post.pk])

        for template, surface in self.CONTRAST_SURFACES.items():
            with self.subTest(template=template):
                self.author.profile.template = template
                self.author.profile.save(update_fields=["template"])
                for render_url in (url, detail_url):
                    response = self.client.get(render_url, follow=True)
                    self.assertEqual(response.status_code, 200)
                    content = response.content.decode(response.charset)
                    self.assertIn(surface, content)
                    self.assertIn("@media (max-width: 576px)", content)

        self.author.profile.template = "default"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(url)
        content = response.content.decode(response.charset)
        self.assertNotIn("--bp-mobile-comment-surface:", content)
