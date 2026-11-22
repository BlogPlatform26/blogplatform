from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.db.models import prefetch_related_objects
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Follow, HomeFeaturedPost, Notification, PollOption, PollVote, Post, QuizAnswer, QuizOption
from .services import enrich_posts_with_quiz_poll_data, publish_due_home_featured_posts, publish_due_posts


class FeedPerformanceTests(TestCase):
    def setUp(self):
        users = get_user_model().objects
        self.author = users.create_user(username='author')
        self.reader = users.create_user(username='reader')
        self.now = timezone.now()

    def create_post(self, title, **fields):
        fields.setdefault('status', 'published')
        fields.setdefault('publish_at', self.now)
        return Post.objects.create(
            author=self.author, title=title, content='<p>Content</p>', **fields,
        )

    def test_featured_page_enriches_only_two_visible_groups(self):
        posts = [self.create_post(f'Post {i}') for i in range(21)]
        for i, post in enumerate(posts):
            HomeFeaturedPost.objects.create(
                post=post, featured_at=self.now - timedelta(minutes=i),
                slot_date=timezone.localdate(self.now), source='algorithm',
            )
        with patch('blog.view_handlers.blog_views.apply_blog_preferences_to_posts') as enrich:
            response = self.client.get(reverse('home'), {'filter': 'featured', 'page': 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['featured_primary_posts'], posts[6:12])
        self.assertEqual(response.context['featured_secondary_posts'], posts[12:18])
        self.assertEqual(response.context['featured_page'].paginator.count, 21)
        enrich.assert_called_once_with(posts[6:18])

    def test_all_and_following_enrich_only_the_requested_page(self):
        Follow.objects.create(follower=self.reader, following=self.author)
        self.client.force_login(self.reader)
        for i in range(12):
            self.create_post(f'Post {i}', publish_at=self.now - timedelta(minutes=i))
        for feed in ('all', 'following'):
            with self.subTest(feed=feed):
                with patch('blog.view_handlers.blog_views.apply_blog_preferences_to_posts') as enrich:
                    response = self.client.get(reverse('home'), {'filter': feed, 'page': 2})
                self.assertEqual(response.status_code, 200)
                page = enrich.call_args.args[0]
                self.assertEqual([post.title for post in page], [f'Post {i}' for i in range(5, 10)])
                enrich.assert_called_once()

    def test_interaction_enrichment_batches_queries_and_keeps_results(self):
        polls = [self.create_post(f'Poll {i}', post_type='poll') for i in range(2)]
        for poll in polls:
            voted = PollOption.objects.create(post=poll, text='Voted')
            PollOption.objects.create(post=poll, text='Empty')
            PollVote.objects.create(post=poll, user=self.reader, option=voted)
        quiz = self.create_post('Quiz', post_type='quiz')
        correct = QuizOption.objects.create(post=quiz, text='Correct', is_correct=True)
        answer = QuizAnswer.objects.create(post=quiz, user=self.reader, selected_option=correct)
        prefetch_related_objects(polls, 'poll_options')
        with patch('blog.services.apply_blog_preferences_to_profile'):
            with self.assertNumQueries(3):
                enrich_posts_with_quiz_poll_data([*polls, quiz], self.reader)
        for poll in polls:
            self.assertEqual(poll.poll_total, 1)
            self.assertEqual(poll.poll_user_vote.user_id, self.reader.pk)
            self.assertEqual(sorted(row['percent'] for row in poll.poll_results), [0, 100])
        self.assertEqual(quiz.quiz_user_answer, answer)
        self.assertTrue(quiz.quiz_is_correct)

    def test_due_publications_and_featured_slots_are_repeatable(self):
        due = self.create_post('Due', status='scheduled', publish_at=self.now - timedelta(minutes=1))
        future = self.create_post('Future', status='scheduled', publish_at=self.now + timedelta(hours=1))
        publish_due_posts()
        publish_due_posts()
        due.refresh_from_db()
        future.refresh_from_db()
        self.assertEqual(due.status, 'published')
        self.assertEqual(future.status, 'scheduled')
        publish_due_home_featured_posts(now=self.now)
        slots = set(HomeFeaturedPost.objects.values_list('slot_token', flat=True))
        self.assertTrue(slots)
        publish_due_home_featured_posts(now=self.now)
        self.assertEqual(HomeFeaturedPost.objects.count(), len(slots))

    def test_home_and_notifications_show_unread_notification(self):
        self.client.force_login(self.reader)
        notification = Notification.objects.create(
            recipient=self.reader, sender=self.author, notification_type='follow',
        )
        home = self.client.get(reverse('home'), {'filter': 'all'})
        self.assertEqual(home.context['unread_notifications_count'], 1)
        notifications = self.client.get(reverse('notifications'))
        self.assertEqual(list(notifications.context['notifications']), [notification])
        destination = self.client.get(reverse('notification_redirect', args=[notification.pk]))
        self.assertRedirects(destination, reverse('user_blog', args=[self.author.username]))
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)
