from django.test import TestCase
from django.urls import reverse


class PublicPasswordResetTests(TestCase):
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
