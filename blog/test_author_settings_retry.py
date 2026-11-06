from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthorSettingsRetryTests(TestCase):
    def test_invalid_profile_preserves_input_and_shows_field_error(self):
        user = User.objects.create_user(username='author-retry')
        profile = user.profile
        profile.author_bio = 'Saved biography'
        profile.save()
        self.client.force_login(user)
        url = reverse('blog_settings') + '?tab=autor'
        response = self.client.post(url, {
            'save_author_profile': '1',
            'author_bio': 'Unsaved biography to retain',
            'author_birth_date': 'not-a-date',
            'author_contact': 'Synthetic contact draft',
            'allow_author_questions': 'on',
        })
        profile.refresh_from_db()
        self.assertEqual(profile.author_bio, 'Saved biography')
        self.assertEqual(response.status_code, 200)
        form = response.context['author_form']
        self.assertTrue(form.is_bound)
        self.assertEqual(form['author_bio'].value(), 'Unsaved biography to retain')
        self.assertEqual(form['author_contact'].value(), 'Synthetic contact draft')
        self.assertIn('author_birth_date', form.errors)
        self.assertContains(response, 'id_author_birth_date_error')
        corrected = self.client.post(url, {
            'save_author_profile': '1',
            'author_bio': 'Unsaved biography to retain',
            'author_birth_date': '2000-01-02',
            'author_contact': 'Synthetic contact draft',
            'allow_author_questions': 'on',
        })
        self.assertEqual(corrected.status_code, 302)
        profile.refresh_from_db()
        self.assertEqual(profile.author_bio, 'Unsaved biography to retain')
        self.assertEqual(profile.author_contact, 'Synthetic contact draft')
        self.assertEqual(profile.author_birth_date.isoformat(), '2000-01-02')
        self.assertTrue(profile.allow_author_questions)
