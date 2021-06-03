"""Test create status."""

from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse_lazy

from statuses.models import Statuses


class TestStatusesCreateView(TestCase):
    """Test create."""

    def setUp(self):
        """Preparate data."""
        self.user = User.objects.create(username='testuser')
        self.user.set_password('12345')
        self.user.save()
        self.status = Statuses.objects.create(name='Тест')
        self.status.save()
        self.url_delete = reverse_lazy(
            'statuses-delete',
            kwargs={'pk': self.status.pk},
        )
        self.url_update = reverse_lazy(
            'statuses-update',
            kwargs={'pk': self.status.pk},
        )
        self.client = Client()

    def test_create(self):
        """Test create status."""
        response = self.client.get(reverse_lazy('login'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.post(
            reverse_lazy('login'),
            data={
                'username': 'testuser',
                'password': '12345',
            },
        )

        response = self.client.get(reverse_lazy('statuses'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.get(reverse_lazy('statuses-create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

        status = {'name': 'Тестовый статус'}
        response = self.client.post(
            reverse_lazy('statuses-create'),
            data=status,
        )
        self.assertRedirects(response, reverse_lazy('statuses'))
        self.assertTrue(Statuses.objects.filter(name=status['name']))

        response = self.client.post(
            reverse_lazy('statuses-create'),
            data=status,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_delete(self):
        """Test delete status."""
        self.assertTrue(Statuses.objects.filter(name='Тест'))
        response = self.client.get(self.url_delete)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        response = self.client.post(
            reverse_lazy('login'),
            data={
                'username': 'testuser',
                'password': '12345',
            },
        )
        response = self.client.get(reverse_lazy('statuses'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.post(self.url_delete)
        self.assertRedirects(response, reverse_lazy('statuses'))
        self.assertFalse(Statuses.objects.filter(name='Тест'))

    def test_update(self):
        """Test update status."""
        self.assertTrue(Statuses.objects.filter(name='Тест'))
        response = self.client.get(self.url_update)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        response = self.client.post(
            reverse_lazy('login'),
            data={
                'username': 'testuser',
                'password': '12345',
            },
        )
        response = self.client.get(reverse_lazy('statuses'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.post(
            self.url_update,
            data={'name': 'Тсет'},
        )
        self.assertRedirects(response, reverse_lazy('statuses'))
        self.assertTrue(Statuses.objects.filter(name='Тсет'))
