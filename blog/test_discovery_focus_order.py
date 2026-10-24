from html.parser import HTMLParser

from django.test import TestCase
from django.urls import reverse


class FocusOrderParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.controls = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a' and 'filter-link' in attrs.get('class', '').split():
            self.controls.append('filter')
        elif tag == 'input' and attrs.get('name') == 'request_type':
            self.controls.append('support')


class DiscoveryFocusOrderTests(TestCase):
    def assert_filters_before_support(self, route, params):
        response = self.client.get(reverse(route), params)
        self.assertEqual(response.status_code, 200)
        parser = FocusOrderParser()
        parser.feed(response.content.decode())
        self.assertIn('filter', parser.controls)
        self.assertIn('support', parser.controls)
        self.assertLess(parser.controls.index('filter'), parser.controls.index('support'))

    def test_home_renders_filters_before_support_without_javascript(self):
        self.assert_filters_before_support('home', {'filter': 'all'})

    def test_search_renders_filters_before_support_without_javascript(self):
        self.assert_filters_before_support('search', {'q': 'example', 'scope': 'posts'})
