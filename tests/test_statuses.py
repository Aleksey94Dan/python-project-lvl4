"""Test status of views"""


from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from user.models import User
from statuses.models import Status


class TestStatusView(TestCase):
    """CRUD tests"""

    fixtures = ['statuses.json', 'users.json', 'labels.json', 'tasks.json']

    @classmethod
    def setUpTestData(cls):
        """User initialization."""
        cls.User = get_user_model()

    def assert_statuses_in_html(self, statuses, html):
        for status in statuses:
            self.assertInHTML(str(status.id), html)
            self.assertInHTML(status.name, html)

    def test_users_list(self):
        login = self.client.login(username='123', password='123')
        statuses = Status.objects.all()
        response = self.client.get(reverse_lazy('statuses'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('statuses', response.context)
        self.assertCountEqual(statuses, response.context.get('statuses'))
        self.assert_statuses_in_html(statuses, response.content.decode())

    def test_create_status(self):
        self.client.login(username='123', password='123')
        response = self.client.post(
            reverse_lazy('statuses-create'),
            follow=True,
            data={'name': 'demo'},
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('Status created successfully', response.content.decode())
        self.assertTrue(Status.objects.filter(name='demo'))

    def test_create_same_status(self):
        self.client.login(username='123', password='123')
        status = Status.objects.all()[:1][0]
        response = self.client.post(
            reverse_lazy('statuses-create'),
            follow=True,
            data={'name': status.name},
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            'Status with this Name already exists.',
            response.content.decode(),
        )

    def test_update_status(self):
        self.client.login(username='123', password='123')
        status = Status.objects.all()[:1][0]
        pk = status.pk
        response = self.client.post(
            reverse_lazy('statuses-update', kwargs={'pk': pk}),
            follow=True,
            data={'name': 'altered'},
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            'Status changed successfully',
            response.content.decode(),
        )
        self.assertTrue(Status.objects.filter(pk=pk, name='altered'))

    def test_delete_status(self):
        self.client.login(username='123', password='123')
        status = Status.objects.get(pk=12)
        response = self.client.post(
            reverse_lazy('statuses-delete', kwargs={'pk': 12}),
            follow=True,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            'Status deleted successfully',
            response.content.decode(),
        )
        self.assertFalse(Status.objects.filter(name=status.name))

    def test_status_error404(self):
        self.client.login(username='123', password='123')

        for url in ['statuses-delete', 'statuses-update']:
            response = self.client.post(
                reverse_lazy(url, kwargs={'pk': 999}),
                follow=True,
            )
            self.assertTrue(response.status_code, HTTPStatus.NOT_FOUND)

    def test_delete_status_if_used(self):
        self.client.login(username='123', password='123')
        status = Status.objects.get(pk=6)
        response = self.client.post(
            reverse_lazy('statuses-delete', kwargs={'pk': 6}),
            follow=True,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            'Unable to delete status because it is in use',
            response.content.decode(),
        )
        self.assertTrue(Status.objects.filter(name=status.name))