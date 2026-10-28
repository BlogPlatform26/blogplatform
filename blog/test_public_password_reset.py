from django.test import TestCase
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
