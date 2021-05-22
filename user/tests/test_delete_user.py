"""Testing user delete."""

from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse_lazy


class TestUserDeleteView(TestCase):
    """Test deleted view."""

    def setUp(self):
        """Create a test database."""
        self.user = User.objects.create(username='testuser')
        self.url = reverse_lazy('user-delete', kwargs={'pk': self.user.pk})
        self.client = Client()

    def test_delete(self):
        """Test delete."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse_lazy('home'))
