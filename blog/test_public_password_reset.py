from django.test import Client, TestCase, override_settings
from django.urls import reverse


class PublicPasswordResetTests(TestCase):
    def test_reset_result_pages_use_public_templates(self):
        for name in ['password_reset_done', 'password_reset_complete']:
            with self.subTest(name=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, 'blog/' + name + '.html')
                self.assertTemplateNotUsed(response, 'admin/base_site.html')

    def test_invalid_token_offers_public_retry(self):
        response = self.client.get(reverse('password_reset_confirm', args=['invalid', 'invalid']))
        self.assertTemplateUsed(response, 'blog/password_reset_confirm.html')
        self.assertFalse(response.context['validlink'])
        self.assertContains(response, 'href="' + reverse('password_reset') + '"')
        self.assertTemplateNotUsed(response, 'admin/base_site.html')

    def test_reset_uses_public_template_not_admin_template(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/password_reset_form.html')
        self.assertTemplateUsed(response, 'blog/base.html')
        self.assertTemplateNotUsed(response, 'admin/base_site.html')

    def test_invalid_email_remains_in_public_form(self):
        response = self.client.post(reverse('password_reset'), {'email': 'invalid'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/password_reset_form.html')
        self.assertTrue(response.context['form'].errors.get('email'))

    def test_valid_token_shows_two_password_fields_without_manual_toggles(self):
        from django.contrib.auth import get_user_model
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.encoding import force_bytes
        from django.utils.http import urlsafe_base64_encode

        user = get_user_model().objects.create_user(username='reset-layout-test')
        url = reverse('password_reset_confirm', args=[
            urlsafe_base64_encode(force_bytes(user.pk)),
            default_token_generator.make_token(user),
        ])
        response = self.client.get(url, follow=True)
        self.assertTrue(response.context['validlink'])
        self.assertTemplateUsed(response, 'blog/password_reset_confirm.html')
        self.assertContains(response, 'name="new_password1"', count=1)
        self.assertContains(response, 'name="new_password2"', count=1)
        # The shared initializer supplies the only functional toggle per field.
        self.assertNotContains(response, '<div class="input-group password-toggle-group">')


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class PublicPasswordResetWorkflowTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model
        self.user = get_user_model().objects.create_user(
            username='reset-workflow', email='reset@example.invalid',
            password='Initial-QA-39!river',
        )

    def test_email_link_validation_success_and_token_reuse(self):
        import re
        from urllib.parse import urlsplit
        from django.core import mail

        response = self.client.post(reverse('password_reset'), {'email': self.user.email})
        self.assertRedirects(response, reverse('password_reset_done'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.user.email])
        link = re.search(r'https?://[^\s<>]+/reset/[^\s<>]+', mail.outbox[0].body)
        self.assertIsNotNone(link)
        token_path = urlsplit(link.group(0)).path
        response = self.client.get(token_path, follow=True)
        self.assertTrue(response.context['validlink'])
        form_path = response.request['PATH_INFO']
        old_hash = self.user.password
        response = self.client.post(form_path, {
            'new_password1': 'Replacement-QA-72!forest',
            'new_password2': 'Mismatch-QA-83!stream',
        })
        self.assertTrue(response.context['form'].errors.get('new_password2'))
        self.assertTemplateUsed(response, 'blog/password_reset_confirm.html')
        self.user.refresh_from_db()
        self.assertEqual(self.user.password, old_hash)
        response = self.client.post(form_path, {
            'new_password1': 'Replacement-QA-72!forest',
            'new_password2': 'Replacement-QA-72!forest',
        })
        self.assertRedirects(response, reverse('password_reset_complete'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('Replacement-QA-72!forest'))
        self.assertFalse(self.user.check_password('Initial-QA-39!river'))
        self.assertTrue(Client().login(username=self.user.username, password='Replacement-QA-72!forest'))
        reused = Client().get(token_path, follow=True)
        self.assertFalse(reused.context['validlink'])
        self.assertTemplateUsed(reused, 'blog/password_reset_confirm.html')

    @override_settings(PASSWORD_RESET_TIMEOUT=60)
    def test_expired_token_keeps_password_and_offers_retry(self):
        from datetime import datetime, timedelta
        from unittest.mock import patch
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.encoding import force_bytes
        from django.utils.http import urlsafe_base64_encode

        issued_at = datetime(2026, 1, 1, 12, 0, 0)
        with patch.object(default_token_generator, '_now', return_value=issued_at):
            token = default_token_generator.make_token(self.user)
        path = reverse('password_reset_confirm', args=[
            urlsafe_base64_encode(force_bytes(self.user.pk)), token,
        ])
        with patch.object(default_token_generator, '_now', return_value=issued_at + timedelta(seconds=61)):
            response = self.client.get(path, follow=True)
        self.assertFalse(response.context['validlink'])
        self.assertTemplateUsed(response, 'blog/password_reset_confirm.html')
        self.assertContains(response, 'href="' + reverse('password_reset') + '"')
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('Initial-QA-39!river'))
