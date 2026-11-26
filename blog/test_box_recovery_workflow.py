from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from blog.models import UserBox


class BoxRecoveryWorkflowTests(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user(username='box-recovery-owner')
        self.client.force_login(self.owner)
        self.box = UserBox.objects.create(user=self.owner, title='Saved title',
                                          content='<p>Saved content</p>', position='left')

    def test_invalid_edit_retains_draft_without_changing_saved_box(self):
        response = self.client.post(reverse('edit_box', args=[self.box.pk]), {
            'title': '   ', 'content': '<p>Unsaved draft must survive</p>', 'position': 'right'})
        self.box.refresh_from_db()
        self.assertEqual(self.box.title, 'Saved title')
        self.assertEqual(self.box.content, '<p>Saved content</p>')
        self.assertEqual(self.box.position, 'left')
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.context['form'].is_bound)
        self.assertEqual(response.context['form']['content'].value(), '<p>Unsaved draft must survive</p>')
        self.assertEqual(response.context['form']['position'].value(), 'right')
        self.assertContains(response, 'id="id_title_error"', status_code=400)

    def test_invalid_add_exposes_field_error_and_preserves_position(self):
        response = self.client.post(reverse('add_box'), {
            'title': '   ', 'content': '<p>New draft</p>', 'position': 'right'})
        self.assertEqual(UserBox.objects.filter(user=self.owner).count(), 1)
        self.assertContains(response, 'id="id_title_error"')
        self.assertContains(response, 'value="right" selected')

    def test_full_destination_retains_edit_draft(self):
        for index in range(3):
            UserBox.objects.create(user=self.owner, title=f'Right {index}',
                                   content='', position='right', order=index)
        response = self.client.post(reverse('edit_box', args=[self.box.pk]), {
            'title': 'Draft title', 'content': '<p>Draft content</p>', 'position': 'right'})
        self.box.refresh_from_db()
        self.assertEqual(self.box.title, 'Saved title')
        self.assertEqual(self.box.position, 'left')
        self.assertEqual(response.status_code, 400)
        self.assertIn('position', response.context['form'].errors)
        self.assertEqual(response.context['form']['title'].value(), 'Draft title')

    def test_correction_saves_and_move_appends_to_destination(self):
        for index in range(2):
            UserBox.objects.create(user=self.owner, title=f'Right {index}',
                                   content='', position='right', order=index)
        response = self.client.post(reverse('edit_box', args=[self.box.pk]), {
            'title': 'Corrected', 'content': '<p>Corrected content</p>', 'position': 'right'})
        self.assertEqual(response.status_code, 302)
        self.box.refresh_from_db()
        self.assertEqual(self.box.title, 'Corrected')
        self.assertEqual(self.box.content, '<p>Corrected content</p>')
        self.assertEqual(self.box.position, 'right')
        self.assertEqual(self.box.order, 2)

    def test_other_user_cannot_read_or_update_box(self):
        stranger = get_user_model().objects.create_user(username='box-recovery-stranger')
        self.client.force_login(stranger)
        url = reverse('edit_box', args=[self.box.pk])
        self.assertEqual(self.client.get(url).status_code, 404)
        self.assertEqual(self.client.post(url, {'title': 'Overwrite', 'content': '',
                                              'position': 'right'}).status_code, 404)
        self.box.refresh_from_db()
        self.assertEqual(self.box.title, 'Saved title')

    def test_full_side_add_preserves_draft_without_creating_box(self):
        for index in range(3):
            UserBox.objects.create(user=self.owner, title=f'Right {index}',
                                   content='', position='right', order=index)
        response = self.client.post(reverse('add_box'), {
            'title': 'New draft', 'content': '<p>Keep new draft</p>', 'position': 'right'})
        self.assertEqual(UserBox.objects.filter(user=self.owner).count(), 4)
        self.assertEqual(response.status_code, 200)
        self.assertIn('position', response.context['form'].errors)
        self.assertEqual(response.context['form']['content'].value(), '<p>Keep new draft</p>')
        self.assertContains(response, 'id="id_position_error"')
