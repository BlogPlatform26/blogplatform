from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import Comment, Notification, Post


class NotificationWorkflowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.reader = User.objects.create_user(username="notification-reader")
        cls.other = User.objects.create_user(username="notification-other")
        cls.author = User.objects.create_user(username="notification-author")
        cls.post = Post.objects.create(author=cls.author, title="Notification story",
                                       content="Synthetic story", status="published")
        cls.comment = Comment.objects.create(post=cls.post, author=cls.author,
                                             content="Synthetic reply")

    def notice(self, kind="like", recipient=None, **kwargs):
        return Notification.objects.create(recipient=recipient or self.reader,
                                           sender=self.author, notification_type=kind,
                                           **kwargs)

    def test_list_empty_populated_and_read_state(self):
        self.client.force_login(self.reader)
        self.assertContains(self.client.get(reverse("notifications")), "Nema notifikacija.")
        item = self.notice(post=self.post)
        self.assertContains(self.client.get(reverse("notifications")), "Novo")
        self.assertContains(self.client.get(reverse("notifications")),
                            f'href="{reverse("notification_redirect", args=[item.pk])}" class="list-group-item list-group-item-action"')
        self.client.get(reverse("notification_redirect", args=[item.pk]))
        item.refresh_from_db()
        self.assertTrue(item.is_read)
        self.assertContains(self.client.get(reverse("notifications")), "Pročitano")

    def test_each_destination_and_repeated_open(self):
        self.client.force_login(self.reader)
        for kind in ("follow", "like", "comment", "mention"):
            with self.subTest(kind=kind):
                item = self.notice(kind, post=self.post,
                                   comment=self.comment if kind in ("comment", "mention") else None)
                expected = (reverse("user_blog", args=[self.author.username]) if kind == "follow"
                            else reverse("post_detail", args=[self.post.pk]))
                if kind in ("comment", "mention"):
                    expected += f"#comment-{self.comment.pk}"
                for _ in range(2):
                    response = self.client.get(reverse("notification_redirect", args=[item.pk]))
                    self.assertRedirects(response, expected, fetch_redirect_response=False)
                item.refresh_from_db()
                self.assertTrue(item.is_read)

    def test_recipient_isolation_and_mark_all_requires_post(self):
        own = self.notice(post=self.post)
        foreign = self.notice(recipient=self.other, post=self.post)
        self.client.force_login(self.reader)
        self.assertEqual(self.client.get(reverse("notification_redirect", args=[foreign.pk])).status_code, 404)
        self.assertEqual(self.client.get(reverse("mark_all_notifications_read")).status_code, 405)
        own.refresh_from_db()
        self.assertFalse(own.is_read)
        self.client.post(reverse("mark_all_notifications_read"))
        own.refresh_from_db()
        foreign.refresh_from_db()
        self.assertTrue(own.is_read)
        self.assertFalse(foreign.is_read)

    def test_guest_cannot_read_or_mark_notifications(self):
        item = self.notice(post=self.post)
        for url in (reverse("notifications"), reverse("notification_redirect", args=[item.pk])):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn(reverse("login"), response.url)
        self.client.post(reverse("mark_all_notifications_read"))
        item.refresh_from_db()
        self.assertFalse(item.is_read)
