from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from blog.models import Post


class PostActionRouteOrderTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(username="route-owner", password="test-password")
        cls.other = User.objects.create_user(username="route-other", password="test-password")
        cls.post = Post.objects.create(
            author=cls.owner, title="Route test draft", content="<p>Draft</p>", status="draft"
        )

    def test_specific_actions_resolve_before_slug_route(self):
        for route_name in ("edit_post", "delete_post", "create_comment", "like_post"):
            kwargs = {"pk" if route_name == "create_comment" else "post_id": self.post.pk}
            url = reverse(route_name, kwargs=kwargs)
            with self.subTest(route_name=route_name):
                self.assertEqual(resolve(url).url_name, route_name)
        canonical = reverse(
            "post_detail_slug", kwargs={"post_id": self.post.pk, "post_slug": "route-test-draft"}
        )
        self.assertEqual(resolve(canonical).url_name, "post_detail_slug")

    def test_owner_can_open_edit_form_without_submitting(self):
        self.client.force_login(self.owner)
        response = self.client.get(reverse("edit_post", args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/edit_post.html")
        self.assertContains(response, "Route test draft")

    def test_non_owner_cannot_open_edit_form(self):
        self.client.force_login(self.other)
        response = self.client.get(reverse("edit_post", args=[self.post.pk]))
        self.assertEqual(response.status_code, 404)
