from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from blog.models import Post


class CalendarQueryValidationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(
            username="calendar-query-author",
            password="test-password",
        )
        cls.author.profile.author_bio = "Calendar query validation biography"
        cls.author.profile.save(update_fields=["author_bio"])

        tz = timezone.get_current_timezone()
        cls.leap_post = Post.objects.create(
            author=cls.author,
            title="Leap day post",
            content="<p>Leap day content</p>",
            status="published",
            publish_at=timezone.make_aware(datetime(2024, 2, 29, 12, 0), tz),
        )
        cls.other_february_post = Post.objects.create(
            author=cls.author,
            title="Other February post",
            content="<p>Other February content</p>",
            status="published",
            publish_at=timezone.make_aware(datetime(2024, 2, 28, 12, 0), tz),
        )

    def route_urls(self):
        return (
            reverse("user_blog", args=[self.author.username]),
            reverse("author_detail", args=[self.author.username]),
        )

    def test_invalid_calendar_values_never_raise_on_public_routes(self):
        invalid_queries = (
            {"month": "13"},
            {"year": "2026", "month": "9", "day": "32"},
            {"year": "2026", "month": "2", "day": "31"},
            {"year": "0", "month": "1"},
            {"year": "10000", "month": "1"},
            {"year": "not-a-year", "month": "not-a-month", "day": "not-a-day"},
        )

        for url in self.route_urls():
            for query in invalid_queries:
                with self.subTest(url=url, query=query):
                    response = self.client.get(url, query)
                    self.assertEqual(response.status_code, 200)

    def test_invalid_day_falls_back_to_valid_month(self):
        response = self.client.get(
            reverse("user_blog", args=[self.author.username]),
            {"year": "2024", "month": "2", "day": "31"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["current_year"], 2024)
        self.assertEqual(response.context["current_month_num"], 2)
        self.assertContains(response, self.leap_post.title)
        self.assertContains(response, self.other_february_post.title)

    def test_valid_leap_day_filters_blog_and_keeps_author_calendar(self):
        query = {"year": "2024", "month": "2", "day": "29"}

        blog_response = self.client.get(
            reverse("user_blog", args=[self.author.username]),
            query,
        )
        author_response = self.client.get(
            reverse("author_detail", args=[self.author.username]),
            query,
        )

        self.assertEqual(blog_response.status_code, 200)
        self.assertContains(blog_response, self.leap_post.title)
        self.assertNotContains(blog_response, self.other_february_post.title)
        self.assertEqual(author_response.status_code, 200)
        self.assertEqual(author_response.context["current_year"], 2024)
        self.assertEqual(author_response.context["current_month_num"], 2)
