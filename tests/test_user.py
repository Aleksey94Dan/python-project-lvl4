"""Test views"""

from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.utils.translation import gettext 


from django.test import TestCase 
from django.urls import reverse_lazy

from user.models import User


class TestUserView(TestCase):
    """CRUD tests"""

    fixtures = ['users.json']

    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()


    def assertUsersInHtml(self, users, html):
        for user in users:
            self.assertInHTML(str(user.id), html)
            self.assertInHTML(user.first_name, html)
            self.assertInHTML(user.get_full_name(), html)


    def test_users_list(self):
        users = self.User.objects.all()
        response = self.client.get(reverse_lazy('users-list'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('users', response.context)
        self.assertCountEqual(users, response.context.get('users'))
        self.assertUsersInHtml(users, response.content.decode())

    def test_login_user(self):
        response = self.client.post(
            reverse_lazy('login'),
            follow=True,
            data={'username': "123", "password": "123"},
        )

        self.assertRedirects(response, reverse_lazy('home'))
        self.assertIn('You are logged in', response.content.decode())

    def test_login_error(self):
        response = self.client.post(
            reverse_lazy('login'),
            follow=True,
            data={'username': "123", "password": "321"},
        )


        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
                'Please enter a correct username and password. '
                'Note that both fields may be case-sensitive.',
                response.content.decode(),
            )

    def test_logout_user(self):
        response = self.client.post(
            reverse_lazy('logout'),
            follow=True,
        )

        self.assertRedirects(response, reverse_lazy('home'))
        self.assertIn('You are logged out', response.content.decode())

    def test_register(self):
        response = self.client.post(
            reverse_lazy('user-create'),
            follow=True,
            data={
                'first_name': 'Ivan',
                'last_name': 'Ivanow',
                'username': "ivan",
                "password1": "111",
                "password2": "111",
            },
        )

        self.assertRedirects(response, reverse_lazy('login'))
        self.assertIn('User registered successfully', response.content.decode())
        self.assertTrue(User.objects.filter(username='ivan'))

    def test_register_error(self):
        response = self.client.post(
            reverse_lazy('user-create'),
            follow=True,
            data={
                'first_name': '123',
                'last_name': '123',
                'username': "123",
                "password1": "111",
                "password2": "111",
            },
        )


        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('A user with that username already exists.', response.content.decode())
        self.assertFalse(User.objects.filter(username='ivan'))

    def test_updated(self):
        user = self.User.objects.all()[:1][0]
        useername = user.username

        response = self.client.post(
            reverse_lazy('user-update', kwargs={'pk':  user.pk }),
            follow=True,
            data={
                'first_name': user.first_name, 
                'last_name': user.last_name,
                'username': "ivan",
                "password1": "111",
                "password2": "111",
            },
        )

