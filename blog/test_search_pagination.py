from datetime import timedelta
from html.parser import HTMLParser
from urllib.parse import parse_qs, urlsplit

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from blog.models import Post


class PageLinks(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.links = {}
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a' and attrs.get('rel') in ('next', 'prev'):
            self.links[attrs['rel']] = attrs['href']


class SearchPaginationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        author = User.objects.create_user(username='search-pagination-author')
        cls.query = 'more & less + "quoted"'
        for index in range(7):
            Post.objects.create(
                author=author, title=f'{cls.query} result {index}',
                content='Search pagination content', status='published',
                publish_at=timezone.now() - timedelta(days=index + 1),
            )

    def test_navigation_preserves_query_scope_and_reaches_remaining_results(self):
        for scope in ('all', 'posts'):
            with self.subTest(scope=scope):
                first = self.client.get(reverse('search'), {'q': self.query, 'scope': scope})
                links = PageLinks(first.content.decode()).links
                self.assertNotIn('prev', links)
                self.assertEqual(parse_qs(urlsplit(links['next']).query),
                                 {'q': [self.query], 'scope': [scope], 'page': ['2']})
                second = self.client.get(reverse('search') + links['next'])
                self.assertEqual(second.status_code, 200)
                first_ids = {post.pk for post in first.context['posts']}
                second_ids = {post.pk for post in second.context['posts']}
                self.assertEqual(len(first_ids), 5)
                self.assertEqual(len(second_ids), 2)
                self.assertFalse(first_ids & second_ids)
                back_links = PageLinks(second.content.decode()).links
                self.assertNotIn('next', back_links)
                back = self.client.get(reverse('search') + back_links['prev'])
                self.assertEqual({post.pk for post in back.context['posts']}, first_ids)

    def test_no_pager_for_empty_results_or_non_post_scopes(self):
        for query, scope in (('absent-query', 'posts'), (self.query, 'users'), (self.query, 'tags')):
            response = self.client.get(reverse('search'), {'q': query, 'scope': scope})
            self.assertNotContains(response, 'aria-label="Stranice rezultata pretrage"')
