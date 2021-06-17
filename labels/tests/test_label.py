"""Test create labels."""

from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse_lazy

from labels.models import Label


class TestLabelView(TestCase):
    """Test create labels."""

    def setUp(self):
        """Preparate data."""
        self.user = User.objects.create(username='testuser')
        self.user.set_password('12345')
        self.user.save()
        self.label = Label.objects.create(name='Тест')
        self.label.save()
        self.url_delete = reverse_lazy(
            'labels-delete',
            kwargs={'pk': self.label.pk},
        )
        self.url_update = reverse_lazy(
            'labels-update',
            kwargs={'pk': self.label.pk},
        )
        self.client = Client()

    def test_create(self):
        """Test create labels."""
        response = self.client.get(reverse_lazy('labels-create'))
        self.assertRedirects(response, reverse_lazy('login'))
        response = self.client.post(
            reverse_lazy('login'),
            data={
                'username': 'testuser',
                'password': '12345',
            },
        )
        self.assertRedirects(response, reverse_lazy('home'))
        response = self.client.get(reverse_lazy('labels'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.get(reverse_lazy('labels-create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        label = {'name': 'Тестовая метка'}
        response = self.client.post(
            reverse_lazy('labels-create'),
            data=label,
        )
        self.assertRedirects(response, reverse_lazy('labels'))
        self.assertTrue(Label.objects.filter(name=label['name']))

        response = self.client.post(
            reverse_lazy('labels-create'),
            data=label,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_delete(self):
        """Test delete status."""
        response = self.client.get(self.url_delete)
        self.assertRedirects(response, reverse_lazy('login'))
        response = self.client.post(
            reverse_lazy('login'),
            data={
                'username': 'testuser',
                'password': '12345',
            },
        )
        self.assertRedirects(response, reverse_lazy('home'))
        response = self.client.get(reverse_lazy('labels'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.post(self.url_delete)
        self.assertRedirects(response, reverse_lazy('labels'))
        self.assertFalse(Label.objects.filter(name='Тест'))

    def test_update(self):
        """Test update labels."""
        response = self.client.get(self.url_update)
        self.assertRedirects(response, reverse_lazy('login'))
        response = self.client.post(
            reverse_lazy('login'),
            data={
                'username': 'testuser',
                'password': '12345',
            },
        )
        self.assertRedirects(response, reverse_lazy('home'))
        response = self.client.get(reverse_lazy('labels'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.post(
            self.url_update,
            data={'name': 'Тсет'},
        )
        self.assertRedirects(response, reverse_lazy('labels'))
        self.assertTrue(Label.objects.filter(name='Тсет'))
