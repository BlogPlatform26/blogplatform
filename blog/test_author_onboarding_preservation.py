from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthorOnboardingPreservationTests(TestCase):
    def test_biography_save_preserves_fields_not_in_onboarding(self):
        user = User.objects.create_user(username='onboarding-preservation')
        profile = user.profile
        expected = {'author_contact': 'Synthetic contact', 'author_social_links': 'Synthetic social', 'author_website': 'https://example.test', 'allow_author_questions': True}
        for name, value in expected.items():
            setattr(profile, name, value)
        profile.save()
        self.client.force_login(user)
        response = self.client.post(reverse('author_onboarding'), {'author_bio': 'Updated biography'})
        self.assertEqual(response.status_code, 302)
        profile.refresh_from_db()
        self.assertEqual(profile.author_bio, 'Updated biography')
        self.assertEqual({name: getattr(profile, name) for name in expected}, expected)
