"""Test labels of views"""


from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse_lazy

from labels.models import Label


class TestLabelsView(TestCase):
    """CRUD tests"""

    fixtures = ['statuses.json', 'users.json', 'labels.json', 'tasks.json']

    def assert_labels_in_html(self, labels, html):
        for label in labels:
            self.assertInHTML(str(label.id), html)
            self.assertInHTML(label.name, html)

    def test_labels_list(self):
        self.client.login(username='123', password='123')
        labels = Label.objects.all()
        response = self.client.get(reverse_lazy('labels'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('labels', response.context)
        self.assertCountEqual(labels, response.context.get('labels'))
        self.assert_labels_in_html(labels, response.content.decode())

    def test_create_label(self):
        self.client.login(username='123', password='123')
        response = self.client.post(
            reverse_lazy('labels-create'),
            follow=True,
            data={'name': 'demo'},
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('Label created successfully', response.content.decode())
        self.assertTrue(Label.objects.filter(name='demo'))

    def test_create_same_label(self):
        self.client.login(username='123', password='123')
        label = Label.objects.all()[:1][0]
        response = self.client.post(
            reverse_lazy('labels-create'),
            follow=True,
            data={'name': label.name},
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            'Label with this Name already exists.',
            response.content.decode(),
        )

    def test_update_label(self):
        self.client.login(username='123', password='123')
        label = Label.objects.all()[:1][0]
        pk = label.pk
        response = self.client.post(
            reverse_lazy('labels-update', kwargs={'pk': pk}),
            follow=True,
            data={'name': 'altered'},
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            'Label updated successfully',
            response.content.decode(),
        )
        self.assertTrue(Label.objects.filter(pk=pk, name='altered'))

    def test_delete_label(self):
        self.client.login(username='123', password='123')
        label = Label.objects.get(pk=29)
        response = self.client.post(
            reverse_lazy('labels-delete', kwargs={'pk': 29}),
            follow=True,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            'Label deleted successfully',
            response.content.decode(),
        )
        self.assertFalse(Label.objects.filter(name=label.name))

    def test_labels_error404(self):
        self.client.login(username='123', password='123')

        for url in ['labels-delete', 'labels-update']:
            response = self.client.post(
                reverse_lazy(url, kwargs={'pk': 999}),
                follow=True,
            )
            self.assertTrue(response.status_code, HTTPStatus.NOT_FOUND)

    def test_delete_label_if_used(self):
        self.client.login(username='123', password='123')
        label = Label.objects.get(pk=24)
        response = self.client.post(
            reverse_lazy('labels-delete', kwargs={'pk': 24}),
            follow=True,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            'Cannot remove a label because it is in use',
            response.content.decode(),
        )
        self.assertTrue(Label.objects.filter(name=label.name))
