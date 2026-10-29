from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from blog.models import BugReport


@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    BUG_REPORT_EMAIL='support@example.test',
    DEFAULT_FROM_EMAIL='noreply@example.test',
)
class SupportWorkflowTests(TestCase):
    def post_report(self, **changes):
        data = {'title': 'Synthetic support', 'description': 'Synthetic message',
                'request_type': 'kvar', 'email': 'reader@example.test'}
        data.update(changes)
        return self.client.post(reverse('submit_bug_report'), data,
                                HTTP_REFERER='http://testserver/')

    def test_guest_types_save_and_prepare_email(self):
        for value, stored, label in [('kvar', 'bug', 'KVAR'),
                                     ('pitanje', 'question', 'PITANJE'),
                                     ('prijedlog', 'idea', 'PRIJEDLOG')]:
            with self.subTest(value=value):
                response = self.post_report(request_type=value)
                self.assertRedirects(response, 'http://testserver/', fetch_redirect_response=False)
                report = BugReport.objects.latest('pk')
                self.assertEqual(report.request_type, stored)
                self.assertEqual(report.title, f'[{label}] Synthetic support')
                self.assertIsNone(report.user_id)
                self.assertEqual(report.email, 'reader@example.test')
                self.assertEqual(report.page_url, 'http://testserver/')
                self.assertIn('Synthetic message', report.description)
                message = mail.outbox[-1]
                self.assertEqual(message.to, ['support@example.test'])
                self.assertEqual(message.reply_to, ['reader@example.test'])
                self.assertEqual(message.subject, report.title)
                self.assertEqual(message.body, report.description)
                self.assertTrue(list(get_messages(response.wsgi_request)))
        self.assertEqual(BugReport.objects.count(), 3)
        self.assertEqual(len(mail.outbox), 3)

    def test_invalid_fields_do_not_save_or_send(self):
        for changes in [{'title': ''}, {'description': ''}, {'email': 'invalid'},
                        {'request_type': 'unknown'}]:
            with self.subTest(changes=changes):
                response = self.post_report(**changes)
                self.assertEqual(response.status_code, 302)
                self.assertIn('Nije poslano.', str(list(get_messages(response.wsgi_request))[0]))
        self.assertEqual(BugReport.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_authenticated_report_records_owner_and_optional_email(self):
        user = get_user_model().objects.create_user(username='support-test')
        self.client.force_login(user)
        self.post_report(email='')
        report = BugReport.objects.get()
        self.assertEqual(report.user, user)
        self.assertEqual(report.email, '')
        self.assertIn('Korisnik: support-test', report.description)
        self.assertEqual(mail.outbox[0].reply_to, [])

    def test_mail_failure_retains_report_and_warns(self):
        with patch('blog.view_handlers.interaction_views.EmailMessage.send',
                   side_effect=RuntimeError('synthetic failure')):
            response = self.post_report()
        self.assertEqual(BugReport.objects.count(), 1)
        self.assertIn('Poruka je spremljena, ali mail nije poslan',
                      str(list(get_messages(response.wsgi_request))[0]))
        self.assertEqual(len(mail.outbox), 0)

    def test_get_cannot_create_report(self):
        self.assertEqual(self.client.get(reverse('submit_bug_report')).status_code, 405)
        self.assertEqual(BugReport.objects.count(), 0)
