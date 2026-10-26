from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Comment, Post
from blog.services import set_blog_preferences


class JedroUSutonContrastContractTests(TestCase):
    def test_factory_heading_surfaces_follow_each_color_independently(self):
        self.author.profile.template = "jedro_u_suton"
        self.author.profile.save(update_fields=["template"])
        for title, caption in (("#fff7ee", "#fff5ea"), ("#123456", "#fff5ea"),
                               ("#fff7ee", "#123456"), ("#123456", "#123456")):
            set_blog_preferences(self.author, {"design_customizations": {
                "jedro_u_suton": {"blog_title_color": title, "box_title_color": caption}
            }})
            for url in (reverse("user_blog", args=[self.author.username]),
                        reverse("post_detail", args=[self.post.pk])):
                with self.subTest(title=title, caption=caption, url=url):
                    html = self.client.get(url, follow=True).content.decode()
                    heading_css = html.split("/* Phase103j:")[1].split("</style>")[0]
                    self.assertEqual(".jus-theme .jus-title" in heading_css, title == "#fff7ee")
                    self.assertEqual(".jus-theme .box-title" in heading_css, caption == "#fff5ea")

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="jedro-contrast-author")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Naslov kroz suton",
            content="<p>Sadrzaj posta</p>",
            status="published",
        )
        Comment.objects.create(
            post=cls.post,
            author=cls.author,
            content="Citljiv komentar",
        )

    def test_blog_and_detail_render_stable_action_and_comment_surfaces(self):
        self.author.profile.template = "jedro_u_suton"
        self.author.profile.save(update_fields=["template"])

        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                content = response.content.decode(response.charset)
                self.assertIn("Phase 83c: photo-independent", content)
                self.assertIn("background: #132b3b !important;", content)
                self.assertIn("color: #ffe0ba !important;", content)
                self.assertIn("background: #fff7e9 !important;", content)
                self.assertIn("color: #7a331f !important;", content)

    def test_existing_mobile_comment_palette_is_preserved(self):
        self.author.profile.template = "jedro_u_suton"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(
            reverse("user_blog", args=[self.author.username])
        )
        content = response.content.decode(response.charset)
        self.assertIn("@media (max-width: 576px)", content)
        self.assertIn("background: #fff7e9 !important;", content)
        self.assertIn("border-color: #b59a78 !important;", content)

    def test_other_design_does_not_receive_jedro_contract(self):
        self.author.profile.template = "staza_prema_vrhovima"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(
            reverse("user_blog", args=[self.author.username])
        )
        content = response.content.decode(response.charset)
        self.assertNotIn("Phase 83c: photo-independent", content)
