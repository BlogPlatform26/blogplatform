from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post
from blog.services import set_blog_preferences


class FactorySimplePostTitleContrastTests(TestCase):
    def test_factory_tone_only_applies_to_unchanged_simple_paper_palettes(self):
        cases = (
            ("simple_pattern", "#2f6479"),
            ("simple_image", "#2f6479"),
            ("simple_retro", "#2f6870"),
        )
        for index, (design, tone) in enumerate(cases, start=1201):
            with self.subTest(design=design):
                author = User.objects.create_user(id=index, username=f"phase100d_{design}")
                author.profile.template = design
                author.profile.save(update_fields=["template"])
                post = Post.objects.create(
                    author=author,
                    title="A factory Simple story",
                    content="<p>Readable story</p>",
                    status="published",
                )
                for url in (
                    reverse("user_blog", args=[author.username]),
                    reverse("post_detail", args=[post.pk]),
                ):
                    html = self.client.get(url, follow=True).content.decode()
                    self.assertIn("Phase 100d:", html)
                    self.assertIn(f"--post-title-color: {tone}", html)

                set_blog_preferences(author, {
                    "design_customizations": {
                        design: {"post_title_color": "#123456"},
                    },
                })
                html = self.client.get(reverse("user_blog", args=[author.username]), follow=True).content.decode()
                self.assertNotIn("Phase 100d:", html)

                set_blog_preferences(author, {
                    "design_customizations": {
                        design: {
                            "post_title_color": "#3f7f93" if design != "simple_retro" else "#4a9aa6",
                            "content_background_color": "#f0f0f0",
                        },
                    },
                })
                html = self.client.get(reverse("user_blog", args=[author.username]), follow=True).content.decode()
                self.assertNotIn("Phase 100d:", html)
