"""Testing user update."""

from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse_lazy
from faker import Faker


class TestUserUpdateView(TestCase):
    """Test registration user."""

    def setUp(self):
        """Create a test database."""
        self.user = User.objects.create(username='testuser')
        self.user.set_password('12345')
        self.user.save()
        self.faker = Faker()
        self.client = Client()
        self.url = reverse_lazy('user-update', kwargs={'pk': self.user.pk})

    def test_update_not_logged_in(self):
        """Testing user change if not logged in."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_update_logged_in(self):
        """Testing user change if logged in."""
        response = self.client.get(reverse_lazy('login'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.post(
            reverse_lazy('login'),
            data={
                'username': 'testuser',
                'password': '12345',
            },
        )
        self.assertRedirects(response, reverse_lazy('home'))
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        username = self.faker.user_name()
        password1 = self.faker.password()
        password2 = password1
        response = self.client.post(
            self.url,
            data={
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'password1': password1,
                'password2': password2,
            },
        )
        self.assertTrue(User.objects.filter(username=username))
        self.assertRedirects(response, reverse_lazy('users-list'))
