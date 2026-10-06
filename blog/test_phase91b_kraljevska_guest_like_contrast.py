from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class Phase91bKraljevskaGuestLikeContrastTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username="phase91b-author")
        cls.post = Post.objects.create(author=cls.author, title="Pozornica", content="<p>Sadrzaj</p>", status="published")

    def test_blog_and_detail_render_local_control_contract(self):
        self.author.profile.template = "kraljevska_pozornica"
        self.author.profile.save(update_fields=["template"])
        for url in (reverse("user_blog", args=[self.author.username]), reverse("post_detail", args=[self.post.pk])):
            response = self.client.get(url, follow=True)
            self.assertEqual(response.status_code, 200)
            content = response.content.decode(response.charset)
            self.assertIn("Phase 91b", content)
            self.assertIn("background: #2b0d14 !important", content)
            self.assertIn("color: #fff0e2 !important", content)
