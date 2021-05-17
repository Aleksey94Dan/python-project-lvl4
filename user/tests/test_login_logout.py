"""Testing user login."""


from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse_lazy


class TestLoginLogoutViews(TestCase):
    """Test login and logout."""

    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.user.set_password('12345')
        self.user.save()
        self.client = Client()

    def test_login(self):
        """Test login."""
        response = self.client.post(
            reverse_lazy('login'),
            data={
                'username': 'testuser',
                'password': '12345',
            },
        )
        self.assertRedirects(response, reverse_lazy('home'))

    def test_logout(self):
        """Test logout."""
        response = self.client.post(reverse_lazy('logout'))
        self.assertRedirects(response, reverse_lazy('home'))
