from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class Phase89fZlatnoHeroContrastTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase89f-author")
        cls.post = Post.objects.create(
            author=cls.author,
            title="Zlatni zapis",
            content="<p>Sadrzaj</p>",
            status="published",
        )

    def test_blog_and_detail_render_local_hero_contrast_contract(self):
        self.author.profile.template = "zlatno_polje"
        self.author.profile.blog_tagline = "Zapisi medju klasjem"
        self.author.profile.save(update_fields=["template", "blog_tagline"])
        for url in (
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                content = response.content.decode(response.charset)
                self.assertIn("Phase 89f", content)
                self.assertIn("background: #fff8e4 !important", content)
                self.assertIn("Zapisi medju klasjem", content)

    def test_other_design_does_not_render_gold_hero_contract(self):
        self.author.profile.template = "neonski_grad"
        self.author.profile.save(update_fields=["template"])
        response = self.client.get(reverse("user_blog", args=[self.author.username]))
        self.assertNotIn("Phase 89f", response.content.decode(response.charset))
