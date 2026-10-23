from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from blog.models import HomeFeaturedPost, Post, Tag


class FeaturedLastPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        author = User.objects.create_user(username='featured-pages')
        cls.tag = Tag.objects.create(name='featured-pages')
        for i in range(8):
            post = Post.objects.create(author=author, title=f'Featured {i}',
                                       content='Content', status='published',
                                       publish_at=timezone.now() - timedelta(days=1))
            post.tags.add(cls.tag)
            HomeFeaturedPost.objects.create(post=post, source='admin',
                                            featured_at=timezone.now() - timedelta(minutes=i+1))

    @patch('blog.view_handlers.blog_views.publish_due_home_featured_posts')
    def test_last_page_keeps_previous_without_empty_secondary_heading(self, _publish):
        response = self.client.get(reverse('home'), {'filter':'featured', 'tag':self.tag.name, 'page':2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['featured_primary_posts']), 2)
        self.assertFalse(response.context['featured_secondary_posts'])
        self.assertIn('?page=1&filter=featured&tag=featured-pages', response.content.decode())
        self.assertContains(response, 'Prethodna')
        self.assertNotContains(response, 'Više istaknutih')
