"""Test labels of views"""


from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse_lazy

from tests.mixins import TestSetUpMixin


class TestLabelsView(TestSetUpMixin, TestCase):
    """CRUD tests"""

    def assert_labels_in_html(self, labels, html):
        for label in labels:
            self.assertInHTML(str(label.id), html)
            self.assertInHTML(label.name, html)

    def test_labels_list(self):
        response = self.client.get(reverse_lazy('labels'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('labels', response.context)
        self.assertCountEqual(self.labels, response.context.get('labels'))
        self.assert_labels_in_html(self.labels, response.content.decode())

    def test_create_label(self):
        response = self.client.post(
            reverse_lazy('labels-create'),
            follow=True,
            data={'name': 'demo'},
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('Label created successfully', response.content.decode())
        self.assertTrue(self.labels.get(name='demo'))

    def test_create_same_label(self):
        response = self.client.post(
            reverse_lazy('labels-create'),
            follow=True,
            data={'name': self.label.name},
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            'Label with this Name already exists.',
            response.content.decode(),
        )

    def test_update_label(self):
        response = self.client.post(
            reverse_lazy('labels-update', kwargs={'pk': self.label.pk}),
            follow=True,
            data={'name': 'altered'},
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            'Label updated successfully',
            response.content.decode(),
        )
        self.assertTrue(self.labels.get(pk=self.label.pk, name='altered'))

    def test_delete_label(self):
        label = self.labels.filter(task__isnull=True).first()
        response = self.client.post(
            reverse_lazy('labels-delete', kwargs={'pk': label.id}),
            follow=True,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            'Label deleted successfully',
            response.content.decode(),
        )
        self.assertFalse(self.labels.filter(name=label.name))

    def test_labels_error404(self):
        fake_id = 999
        for url in ['labels-delete', 'labels-update']:
            response = self.client.post(
                reverse_lazy(url, kwargs={'pk': fake_id}),
                follow=True,
            )
            self.assertTrue(response.status_code, HTTPStatus.NOT_FOUND)

    def test_delete_label_if_used(self):
        label = self.labels.filter(task__isnull=False).first()
        response = self.client.post(
            reverse_lazy('labels-delete', kwargs={'pk': label.id}),
            follow=True,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            'Cannot remove a label because it is in use',
            response.content.decode(),
        )
        self.assertTrue(self.labels.get(id=label.id))
