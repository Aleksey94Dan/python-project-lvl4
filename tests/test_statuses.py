"""Test status of views"""


from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse_lazy

from statuses.models import Status
from tests.mixins import AuthMixn, FixturesMixin


class TestStatusView(FixturesMixin, AuthMixn, TestCase):
    """CRUD tests"""

    def setUp(self):
        super().setUp()
        self.statuses = Status.objects.all()
        self.status = self.statuses.first()

    def assert_statuses_in_html(self, statuses, html):
        for status in statuses:
            self.assertInHTML(str(status.id), html)
            self.assertInHTML(status.name, html)

    def test_users_list(self):
        response = self.client.get(reverse_lazy('statuses'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('statuses', response.context)
        self.assertCountEqual(self.statuses, response.context.get('statuses'))
        self.assert_statuses_in_html(self.statuses, response.content.decode())

    def test_create_status(self):
        response = self.client.post(
            reverse_lazy('statuses-create'),
            follow=True,
            data={'name': 'demo'},
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('Status created successfully', response.content.decode())
        self.assertTrue(self.statuses.filter(name='demo').exists())

    def test_create_same_status(self):
        response = self.client.post(
            reverse_lazy('statuses-create'),
            follow=True,
            data={'name': self.status.name},
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            'Status with this Name already exists.',
            response.content.decode(),
        )

    def test_update_status(self):
        response = self.client.post(
            reverse_lazy('statuses-update', kwargs={'pk': self.status.pk}),
            follow=True,
            data={'name': 'altered'},
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            'Status changed successfully',
            response.content.decode(),
        )
        self.assertTrue(
            self.statuses.filter(pk=self.status.pk, name='altered').exists(),
        )

    def test_delete_status(self):
        status = self.statuses.filter(task__isnull=True).first()
        response = self.client.post(
            reverse_lazy('statuses-delete', kwargs={'pk': status.pk}),
            follow=True,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            'Status deleted successfully',
            response.content.decode(),
        )
        self.assertFalse(self.statuses.filter(name=status.name).exists())

    def test_status_error404(self):
        fake_id = 999

        for url in ['statuses-delete', 'statuses-update']:
            response = self.client.post(
                reverse_lazy(url, kwargs={'pk': fake_id}),
                follow=True,
            )
            self.assertTrue(response.status_code, HTTPStatus.NOT_FOUND)

    def test_delete_status_if_used(self):
        status = self.statuses.filter(task__isnull=False).first()
        response = self.client.post(
            reverse_lazy('statuses-delete', kwargs={'pk': status.id}),
            follow=True,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            'Unable to delete status because it is in use',
            response.content.decode(),
        )
        self.assertTrue(self.statuses.filter(id=status.id).exists())
