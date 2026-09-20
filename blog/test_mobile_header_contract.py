from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class MobileHeaderContractTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(
            username="mobile-header-author", password="test-password"
        )
        cls.post = Post.objects.create(
            author=cls.author,
            title="Mobile header post",
            content="<p>Body</p>",
            status="published",
        )

    def test_public_pages_share_responsive_search_contract(self):
        urls = (
            reverse("home"),
            reverse("search") + "?q=mobile",
            reverse("login"),
            reverse("register"),
            reverse("user_blog", args=[self.author.username]),
            reverse("post_detail", args=[self.post.pk]),
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                content = response.content.decode(response.charset)
                self.assertIn(
                    '<meta name="viewport" content="width=device-width, initial-scale=1">',
                    content,
                )
                self.assertIn('id="searchToggleBtn"', content)
                self.assertIn('id="navbarSearchInline"', content)
                self.assertIn("#navbarSearchInline .input-group", content)
                self.assertIn("width: 100% !important;", content)
                self.assertIn("min-width: 44px !important;", content)

    def test_direct_post_forms_keep_mobile_profile_menu_and_guest_login_links(self):
        guest = self.client.get(reverse("home"))
        self.assertContains(guest, 'href="/login/"')
        self.assertContains(guest, 'href="/register/"')

        self.client.force_login(self.author)
        for url in (reverse("create_post"), reverse("edit_post", args=[self.post.pk])):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                html = response.content.decode(response.charset)
                self.assertIn('class="nav-greeting-prefix">Pozdrav, </span>', html)
                self.assertIn('class="nav-user dropdown-toggle"', html)
                self.assertIn('class="dropdown-item" href="/profile/"', html)
                self.assertIn("#globalNavbar .nav-greeting-prefix", html)
                self.assertIn("gap: 6px;", html)
