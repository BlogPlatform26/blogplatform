import re

from django.contrib.auth.models import User
from django.template.loader import get_template
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from blog.models import Comment, Post, Profile, UserBox
from blog.services import (
    POST_DATE_EFFECT_OPTIONS,
    POST_DATE_STYLE_OPTIONS,
    resolve_design_template_name,
    set_blog_preferences,
)


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
    BESPOKE_DATE_DESIGNS = {
        "ponocna_elegancija": "pe-post-date",
        "ruzicasti_vrt": "rv-post-date",
        "stara_aleja": "sa-post-date",
        "staza_prema_vrhovima": "spv-post-date",
        "jedro_u_suton": "jus-post-date",
        "misticno_jezero": "mj-post-date",
    }
    BESPOKE_TITLE_BOX_PREFIXES = {
        "ponocna_elegancija": "pe",
        "ruzicasti_vrt": "rv",
        "stara_aleja": "sa",
        "staza_prema_vrhovima": "spv",
        "jedro_u_suton": "jus",
        "misticno_jezero": "mj",
    }

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
                    self.assertContains(
                        response,
                        "data-post-primary-date",
                        count=1,
                        html=False,
                    )
                    self.assertContains(
                        response,
                        'id="blogplatform-date-style-contract"',
                        count=1,
                        html=False,
                    )
                    publication_datetime = timezone.localtime(
                        self.post.publication_datetime
                    )
                    duplicate_author_line_date = publication_datetime.strftime(
                        "%d.%m.%Y %H:%M"
                    )
                    content = response.content.decode(response.charset)
                    author_line = re.search(
                        r'<span class="post-author-line">(.*?)</div>',
                        content,
                        flags=re.DOTALL,
                    )
                    self.assertIsNotNone(author_line)
                    self.assertIn(
                        duplicate_author_line_date,
                        author_line.group(1),
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

    def test_shared_date_style_contract_preserves_all_style_families(self):
        self.author.profile.template = "nebeska_klasika"
        self.author.profile.save(update_fields=["template"])

        response = self.client.get(
            reverse("user_blog", args=[self.author.username])
        )
        content = response.content.decode(response.charset)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content.count('id="blogplatform-date-style-contract"'), 1)
        self.assertIn(
            "--date-scale-factor: calc(var(--post-date-scale, 100) / 100);",
            content,
        )
        self.assertIn(".blog-date-shell.blog-date-effect-solid", content)
        self.assertIn(".blog-date-shell.blog-date-effect-duo", content)
        self.assertIn(".blog-date-shell.blog-date-effect-gradient", content)
        for style in (
            "classic_vertical",
            "slim_vertical",
            "card",
            "minimal_inline",
            "split",
            "ribbon",
            "boxed_number",
            "corner_tag",
            "soft",
            "newspaper",
        ):
            with self.subTest(style=style):
                self.assertIn(f".blog-date-style-{style}", content)
        self.assertIn(
            ".blog-date-shell.blog-date-style-minimal_inline .blog-date-main,",
            content,
        )
        self.assertIn(
            ".blog-date-shell.blog-date-style-minimal_inline .blog-date-inline,",
            content,
        )
        self.assertIn(
            ".blog-date-shell.blog-date-style-split .blog-date-main,",
            content,
        )

    def test_bespoke_dates_reach_every_shared_style_effect_and_scale(self):
        url = reverse("user_blog", args=[self.author.username])
        styles = tuple(POST_DATE_STYLE_OPTIONS)
        effects = tuple(POST_DATE_EFFECT_OPTIONS)
        self.assertEqual(len(styles), 10)
        self.assertEqual(len(effects), 3)

        for template_index, (template_key, wrapper_class) in enumerate(
            self.BESPOKE_DATE_DESIGNS.items()
        ):
            self.author.profile.template = template_key
            self.author.profile.save(update_fields=["template"])
            observed_effects = set()

            for style_index, style in enumerate(styles):
                effect = effects[style_index % len(effects)]
                scale = str(70 + (template_index * 10) + (style_index * 5))
                observed_effects.add(effect)
                set_blog_preferences(self.author, {
                    "design_customizations": {
                        template_key: {
                            "post_date_style": style,
                            "post_date_effect": effect,
                            "post_date_size": scale,
                        },
                    },
                })

                with self.subTest(template=template_key, style=style, effect=effect):
                    response = self.client.get(url)
                    content = response.content.decode(response.charset)
                    self.assertEqual(response.status_code, 200)
                    self.assertContains(response, "data-post-primary-date", count=1)
                    self.assertIn(
                        f'class="{wrapper_class} blog-date-shell '
                        f'blog-date-style-{style} blog-date-effect-{effect}"',
                        content,
                    )
                    self.assertIn('class="blog-date-main"', content)
                    self.assertIn('class="blog-date-inline"', content)
                    self.assertIn(f"--post-date-scale: {scale};", content)

            self.assertEqual(observed_effects, set(effects))

    def test_bespoke_visible_title_and_box_targets_use_editor_variables(self):
        UserBox.objects.create(
            user=self.author,
            title="Bespoke hook box",
            content="Hook box body",
            position="left",
        )
        url = reverse("user_blog", args=[self.author.username])

        for template_key, prefix in self.BESPOKE_TITLE_BOX_PREFIXES.items():
            with self.subTest(template=template_key):
                self.author.profile.template = template_key
                self.author.profile.save(update_fields=["template"])
                set_blog_preferences(self.author, {
                    "analytics_live_counter_enabled": True,
                    "design_customizations": {
                        template_key: {
                            "blog_title_font": "tahoma",
                            "blog_title_color": "#123456",
                            "blog_title_size": "67",
                            "box_title_font": "verdana",
                            "box_title_color": "#654321",
                            "box_title_size": "23",
                        },
                    },
                })

                response = self.client.get(url)
                content = response.content.decode(response.charset)
                self.assertEqual(response.status_code, 200)
                self.assertIn(
                    f'class="{prefix}-title blog-page-title"',
                    content,
                )
                self.assertIn(
                    f'class="{prefix}-side-title box-title">O autoru',
                    content,
                )
                self.assertIn(
                    f'class="{prefix}-calendar-title box-title">Kalendar',
                    content,
                )
                self.assertIn(
                    f'class="{prefix}-archive-title box-title">Arhiva bloga',
                    content,
                )
                self.assertIn(
                    f'class="{prefix}-box-title box-title">Bespoke hook box',
                    content,
                )
                self.assertIn(
                    'class="sidebar-box-title">Posjetitelji',
                    content,
                )
                self.assertIn("--blog-title-color: #123456;", content)
                self.assertIn("--blog-title-size: 67px;", content)
                self.assertIn("--box-title-color: #654321;", content)
                self.assertIn("--box-title-size: 23px;", content)
                self.assertIn(
                    "font-family: var(--box-title-font, Georgia",
                    content,
                )
                self.assertNotIn("Hook box body blog-page-title", content)

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

    def test_simple_retro_archive_modes_are_exclusive_and_keep_blog_routes(self):
        self.author.profile.template = "simple_retro"
        self.author.profile.save(update_fields=["template"])
        url = reverse("user_blog", args=[self.author.username])

        for mode, expect_calendar, expect_archive in (
            ("both", True, True),
            ("calendar", True, False),
            ("list", False, True),
        ):
            with self.subTest(mode=mode):
                set_blog_preferences(self.author, {"blog_archive_mode": mode})
                response = self.client.get(url)
                content = response.content.decode(response.charset)
                self.assertEqual(response.status_code, 200)
                self.assertEqual('class="calendar-box calendar-box--simple"' in content, expect_calendar)
                self.assertEqual('class="archive-box archive-box--simple"' in content, expect_archive)
                if expect_calendar:
                    self.assertIn('aria-label="Prethodni mjesec"', content)
                    self.assertIn('aria-label="Sljedeći mjesec"', content)
                if expect_archive:
                    self.assertIn(f'href="{url}?year=', content)

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
        self.assertNotIn("calc(100vw - 290px)", content)
        self.assertIn("max-width: calc(100% - 290px) !important;", content)
        self.assertIn("width: calc(100% - 290px) !important;", content)
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

    def test_nebeska_klasika_editor_targets_use_shared_contract(self):
        self.author.profile.template = "nebeska_klasika"
        self.author.profile.save(update_fields=["template"])
        UserBox.objects.create(
            user=self.author,
            title="Nebeska test box",
            content="Box content",
            position="left",
        )

        response = self.client.get(
            reverse("user_blog", args=[self.author.username])
        )
        content = response.content.decode(response.charset)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/designs/nebeska_klasika.html")
        self.assertIn('class="nk-title blog-page-title"', content)
        self.assertIn('class="mb-0 blog-post-title"', content)
        self.assertIn('class="nk-side-title box-title">O autoru', content)
        self.assertIn('class="nk-calendar-title box-title">Kalendar', content)
        self.assertIn('class="nk-archive-title box-title">Arhiva bloga', content)
        self.assertIn(
            'class="nk-box-title box-title">Nebeska test box',
            content,
        )
        self.assertIn('class="nk-post-date blog-date-shell ', content)
        self.assertIn('class="blog-date-main"', content)
        self.assertIn('class="blog-date-inline"', content)
        self.assertIn("font-family: var(--blog-title-font, Georgia", content)
        self.assertIn("font-size: var(--blog-title-size, clamp(1.7rem", content)
        self.assertIn("color: var(--blog-title-color, #514d57)", content)
        self.assertIn("font-family: var(--post-title-font, Georgia", content)
        self.assertIn("font-size: var(--post-title-size, clamp(1.8rem", content)
        self.assertIn("font-family: var(--box-title-font, Georgia", content)
        self.assertIn("color: var(--box-title-color, #584d46)", content)
