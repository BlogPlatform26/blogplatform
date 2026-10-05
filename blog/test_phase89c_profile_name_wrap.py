from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class Phase89cProfileNameWrapTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(
            username="phase89c_profile_name_without_spaces",
        )
        cls.post = Post.objects.create(
            author=cls.author,
            title="Sidebar ime",
            content="<p>Sadrzaj</p>",
            status="published",
        )

    def test_representative_right_sidebars_render_shared_name_wrap_contract(self):
        for template in ("polje_lavande", "neonski_grad"):
            self.author.profile.template = template
            self.author.profile.save(update_fields=["template"])

            for url in (
                reverse("user_blog", args=[self.author.username]),
                reverse("post_detail", args=[self.post.pk]),
            ):
                with self.subTest(template=template, url=url):
                    response = self.client.get(url, follow=True)
                    self.assertEqual(response.status_code, 200)
                    content = response.content.decode(response.charset)
                    self.assertIn(".blog-profile-panel__name", content)
                    self.assertIn("overflow-wrap: anywhere", content)
