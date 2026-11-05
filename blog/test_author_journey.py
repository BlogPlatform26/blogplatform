from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blog.models import AuthorQuestion


class AuthorJourneyTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username='author-journey')
        cls.reader = User.objects.create_user(username='author-reader')
        profile = cls.author.profile
        profile.author_bio = 'Existing synthetic biography'
        profile.allow_author_questions = True
        profile.save()

    def test_reader_question_validation_and_persistence(self):
        self.client.force_login(self.reader)
        url = reverse('submit_author_question', args=[self.author.username])
        self.assertEqual(self.client.get(url).status_code, 405)
        for value in ('', '  ', 'ab', 'x' * 1201):
            with self.subTest(value_length=len(value)):
                self.client.post(url, {'question': value})
                self.assertFalse(AuthorQuestion.objects.exists())
        self.client.post(url, {'question': '  Synthetic question?  '})
        item = AuthorQuestion.objects.get()
        self.assertEqual(item.question, 'Synthetic question?')
        self.assertEqual(item.author, self.author)
        self.assertEqual(item.sender, self.reader)
        self.assertFalse(item.is_public)

    def test_owner_and_disabled_questions_do_not_save(self):
        url = reverse('submit_author_question', args=[self.author.username])
        self.client.force_login(self.author)
        self.client.post(url, {'question': 'Self question?'})
        self.client.force_login(self.reader)
        profile = self.author.profile
        profile.allow_author_questions = False
        profile.save()
        self.client.post(url, {'question': 'Disabled question?'})
        self.assertFalse(AuthorQuestion.objects.exists())

    def test_onboarding_save_skip_and_invalid_date(self):
        self.client.force_login(self.author)
        url = reverse('author_onboarding')
        self.client.post(url, {'skip_author_onboarding': '1', 'author_bio': 'Discard me'})
        self.author.profile.refresh_from_db()
        self.assertEqual(self.author.profile.author_bio, 'Existing synthetic biography')
        response = self.client.post(url, {'author_bio': 'Invalid save', 'author_birth_date': 'not-a-date'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['author_form'].errors)
        self.author.profile.refresh_from_db()
        self.assertEqual(self.author.profile.author_bio, 'Existing synthetic biography')
        self.client.post(url, {'author_bio': 'Saved synthetic biography'})
        self.author.profile.refresh_from_db()
        self.assertEqual(self.author.profile.author_bio, 'Saved synthetic biography')

    def test_guest_cannot_submit(self):
        for name, args in [('author_onboarding', []), ('submit_author_question', [self.author.username])]:
            response = self.client.post(reverse(name, args=args), {'question': 'Guest question?'})
            self.assertEqual(response.status_code, 302)
            self.assertIn('/login/', response.url)
        self.assertFalse(AuthorQuestion.objects.exists())
