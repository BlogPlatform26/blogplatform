from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class Phase95c2AsfaltniHeroContrastTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase95c2-author")
        cls.author.profile.template = "asfaltni_plamen"
        cls.author.profile.blog_name = "Asfaltni plamen"
        cls.author.profile.blog_tagline = "Priče s ceste"
        cls.author.profile.save(update_fields=["template", "blog_name", "blog_tagline"])
        cls.post = Post.objects.create(
            author=cls.author,
            title="Probna vožnja",
            content="<p>Probni sadržaj</p>",
            status="published",
        )

    def test_local_hero_protection_on_blog_and_detail(self):
        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            response = self.client.get(url, follow=True)
            self.assertEqual(response.status_code, 200)
            content = response.content.decode(response.charset)
            self.assertIn("Phase 95c2: protect only the lettering", content)
            self.assertIn(".blog-header-main .blog-page-subtitle", content)
            self.assertIn("background: #21140e !important", content)
            self.assertIn("color: #f4e7d8 !important", content)
            self.assertIn("overflow-wrap: anywhere", content)

    def test_other_design_does_not_render_asfaltni_hero_rule(self):
        self.author.profile.template = "default"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(
            "Phase 95c2: protect only the lettering",
            response.content.decode(response.charset),
        )
