from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from blog.models import Follow, Post


class HomeFollowingTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(username='following-owner')
        cls.reader = User.objects.create_user(username='following-reader')
        cls.other = User.objects.create_user(username='following-other')
        cls.post = Post.objects.create(
            author=cls.owner, title='Followed author post', content='Content',
            status='published', publish_at=timezone.now() - timedelta(days=1),
        )
        Post.objects.create(
            author=cls.other, title='Unfollowed author post', content='Content',
            status='published', publish_at=timezone.now() - timedelta(days=1),
        )
        Follow.objects.create(follower=cls.reader, following=cls.owner)

    def test_guest_personal_filter_uses_public_default(self):
        response = self.client.get(reverse('home'), {'filter': 'following'})
        default = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['filter_type'], 'featured')
        self.assertEqual(list(response.context['posts']), list(default.context['posts']))
        self.assertNotContains(response, 'Postovi korisnika koje pratiš')

    def test_reader_only_sees_followed_author(self):
        self.client.force_login(self.reader)
        response = self.client.get(reverse('home'), {'filter': 'following'})
        self.assertEqual([post.pk for post in response.context['posts']], [self.post.pk])
        self.assertContains(response, 'Postovi korisnika koje pratiš')
        self.assertNotContains(response, 'Unfollowed author post')

    def test_owner_without_follows_has_empty_feed_not_own_posts(self):
        self.client.force_login(self.owner)
        response = self.client.get(reverse('home'), {'filter': 'following'})
        self.assertFalse(list(response.context['posts']))
        self.assertContains(response, 'Nema postova.')
        self.assertNotContains(response, 'Followed author post')

    def test_all_feed_still_includes_both_authors(self):
        response = self.client.get(reverse('home'), {'filter': 'all'})
        self.assertEqual(response.context['posts'].paginator.count, 2)
