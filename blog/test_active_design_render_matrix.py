from django.contrib.auth.models import User
from django.template.loader import get_template
from django.test import TestCase
from django.urls import reverse

from blog.models import Comment, Post, Profile
from blog.services import resolve_design_template_name, set_blog_preferences


class ActiveDesignRenderMatrixTests(TestCase):
    POST_TITLE = "Registry matrix post"
    POST_BODY = "Registry matrix body"
    COMMENT_BODY = "Registry matrix comment"
    CUSTOM_POST_TITLE_COLOR = "#123abc"

    SPECIAL_DESIGNS = frozenset({
        "soho",
        "magazin",
        "nebeska_klasika",
        "ponocna_elegancija",
        "ruzicasti_vrt",
        "stara_aleja",
        "staza_prema_vrhovima",
        "jedro_u_suton",
        "misticno_jezero",
    })

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(
            username="design-matrix-author",
            password="test-password",
        )
        cls.author.profile.blog_name = "Registry matrix blog"
        cls.author.profile.save(update_fields=["blog_name"])

        cls.post = Post.objects.create(
            author=cls.author,
            title=cls.POST_TITLE,
            content=f"<p>{cls.POST_BODY}</p>",
            status="published",
        )
        cls.commenter = User.objects.create_user(
            username="design-matrix-commenter",
            password="test-password",
        )
        Comment.objects.create(
            post=cls.post,
            author=cls.commenter,
            content=cls.COMMENT_BODY,
        )

        registry_keys = cls.registry_keys()
        set_blog_preferences(cls.author, {
            "blog_archive_mode": "both",
            "design_customizations": {
                key: {"post_title_color": cls.CUSTOM_POST_TITLE_COLOR}
                for key in registry_keys
            },
        })

    @classmethod
    def registry_keys(cls):
        return tuple(key for key, _label in Profile.TEMPLATE_CHOICES)

    def test_every_registered_design_renders_public_blog(self):
        registry = set(self.registry_keys())
        families = {
            "special": self.SPECIAL_DESIGNS,
            "standard_shared": registry - self.SPECIAL_DESIGNS,
        }

        self.assertFalse(families["special"] - registry)
        self.assertFalse(families["special"] & families["standard_shared"])
        self.assertEqual(set().union(*families.values()), registry)
        self.assertEqual(len(registry), len(self.registry_keys()))

        url = reverse("user_blog", args=[self.author.username])
        for family, template_keys in families.items():
            for template_key in sorted(template_keys):
                with self.subTest(family=family, template=template_key):
                    self.author.profile.template = template_key
                    self.author.profile.save(update_fields=["template"])

                    expected_template = resolve_design_template_name(template_key)
                    self.assertIsNotNone(get_template(expected_template))

                    response = self.client.get(url)

                    self.assertEqual(response.status_code, 200)
                    self.assertTemplateUsed(response, expected_template)
                    self.assertContains(response, self.POST_TITLE, html=False)
                    self.assertContains(response, self.POST_BODY, html=False)
                    self.assertContains(
                        response,
                        f'id="comments-{self.post.pk}"',
                        html=False,
                    )
                    self.assertContains(
                        response,
                        f"--post-title-color: {self.CUSTOM_POST_TITLE_COLOR};",
                        html=False,
                    )

                    self.assertEqual(list(response.context["page_obj"]), [self.post])
                    self.assertTrue(
                        self.post.comments.filter(content=self.COMMENT_BODY).exists()
                    )
                    self.assertTrue(response.context["month_calendar"])
                    self.assertTrue(response.context["archives"])
                    self.assertEqual(
                        response.context["blog_preferences"]
                        ["active_design_customization"]["post_title_color"],
                        self.CUSTOM_POST_TITLE_COLOR,
                    )

    def test_terminal_body_theme_css_is_scoped_to_its_intended_family(self):
        url = reverse("user_blog", args=[self.author.username])
        css_expectations = {
            "default": "body { background:#ffffff; color:#1f2937;",
            "dark": "body { background-color:#111; color:#fff;",
            "classic": "body { background:#f6f6f4; color:#1f1f1f;",
            "litica_noci": "background: #000000;",
        }
        default_fallback = css_expectations["default"]

        for template_key, expected_css in css_expectations.items():
            with self.subTest(template=template_key):
                self.author.profile.template = template_key
                self.author.profile.save(update_fields=["template"])

                response = self.client.get(url)
                content = response.content.decode(response.charset)

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, expected_css, html=False)
                if template_key != "default":
                    self.assertNotIn(default_fallback, content)

    def test_soho_mobile_columns_override_fixed_desktop_widths(self):
        self.author.profile.template = "soho"
        self.author.profile.save(update_fields=["template"])

        response = self.client.get(
            reverse("user_blog", args=[self.author.username])
        )
        content = response.content.decode(response.charset)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/designs/studio.html")
        self.assertIn(
            """@media (max-width: 991.98px) {
    .blog-main-left-column,
    .blog-main-content-column {
        flex: 0 0 100% !important;
        max-width: 100% !important;
        width: 100% !important;
    }""",
            content,
        )

    def test_magazin_full_width_css_does_not_use_viewport_width(self):
        self.author.profile.template = "magazin"
        self.author.profile.save(update_fields=["template"])

        response = self.client.get(
            reverse("user_blog", args=[self.author.username])
        )
        content = response.content.decode(response.charset)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/designs/magazin.html")
        self.assertNotIn("width: 100vw !important;", content)
        self.assertNotIn("calc(50% - 50vw)", content)
        self.assertIn(
            """.container-fluid.mt-3 {
    margin-top: 0 !important;
    padding: 0 !important;
    max-width: none !important;
    width: 100% !important;
    margin-left: 0 !important;
    margin-right: 0 !important;
}""",
            content,
        )

    def test_magazin_editor_targets_use_shared_semantic_classes(self):
        self.author.profile.template = "magazin"
        self.author.profile.save(update_fields=["template"])

        response = self.client.get(
            reverse("user_blog", args=[self.author.username])
        )
        content = response.content.decode(response.charset)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/designs/magazin.html")
        self.assertIn('class="magazin-blog-title blog-page-title"', content)
        self.assertIn('class="magazin-section-title box-title">Kalendar', content)
        self.assertIn('class="magazin-calendar-title box-title calendar-month-nav"', content)
        self.assertIn('class="magazin-section-title box-title">Arhiva', content)
