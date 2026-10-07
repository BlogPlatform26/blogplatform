from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class Phase93eSjeneLongTitleTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase93e-author")
        cls.author.profile.template = "sjene_ulice"
        cls.author.profile.blog_name = "SjeneUliceNeprekinutiDugiNaslovZaMobilniPrikaz2026"
        cls.author.profile.save(update_fields=["template", "blog_name"])
        cls.post = Post.objects.create(
            author=cls.author,
            title="Nocna setnja kroz ulicu",
            content="<p>Probni tekst</p>",
            status="published",
        )

    def test_blog_and_detail_include_title_and_profile_wrap(self):
        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                content = response.content.decode(response.charset)
                self.assertIn(self.author.profile.blog_name, content)
                self.assertIn("Phase 93e: keep an unbroken blog name", content)
                self.assertIn("overflow-wrap: anywhere;", content)
                self.assertIn(".blog-profile-panel__blog-name", content)

    def test_other_design_omits_sjene_title_rule(self):
        self.author.profile.template = "default"
        self.author.profile.save(update_fields=["template"])

        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn("Phase 93e: keep an unbroken blog name", response.content.decode(response.charset))
