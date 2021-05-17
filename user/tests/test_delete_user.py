"""Testing user delete."""


from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse_lazy


class TestLoginLogoutViews(TestCase):
    """Test login and logout."""

    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.client = Client()

    def test_delete(self):
        """Test login."""
        response = self.client.post(
            reverse_lazy('user-delete', kwargs={'pk': self.user.pk}),
        )
        self.assertRedirects(response, reverse_lazy('home'))
