"""Test views"""

from http import HTTPStatus

from django.contrib import auth
from django.test import TestCase
from django.urls import reverse_lazy

from tests.mixins import TestSetUpMixin


class TestUserView(TestSetUpMixin, TestCase):
    """CRUD tests"""

    def assert_users_in_html(self, users, html):
        for user in users:
            self.assertInHTML(str(user.id), html)
            self.assertInHTML(user.first_name, html)
            self.assertInHTML(user.get_full_name(), html)

    def test_users_list(self):
        response = self.client.get(reverse_lazy('users-list'))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('users', response.context)
        self.assertCountEqual(self.users, response.context.get('users'))
        self.assert_users_in_html(self.users, response.content.decode())

    def test_login_user(self):
        self.client.logout()
        response = self.client.post(
            reverse_lazy('login'),
            follow=True,
            data={'username': "123", "password": "123"},
        )
        user = auth.get_user(self.client)

        self.assertRedirects(response, reverse_lazy('home'))
        self.assertIn('You are logged in', response.content.decode())
        self.assertTrue(user.is_authenticated)

    def test_login_error(self):
        self.client.logout()
        response = self.client.post(
            reverse_lazy('login'),
            follow=True,
            data={'username': "123", "password": "321"},
        )
        user = auth.get_user(self.client)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(
            'Please enter a correct username and password. '
            'Note that both fields may be case-sensitive.',
            response.content.decode(),
        )
        self.assertFalse(user.is_authenticated)

    def test_logout_user(self):
        response = self.client.post(
            reverse_lazy('logout'),
            follow=True,
        )
        user = auth.get_user(self.client)

        self.assertRedirects(response, reverse_lazy('home'))
        self.assertIn('You are logged out', response.content.decode())
        self.assertFalse(user.is_authenticated)

    def test_register(self):
        response = self.client.post(
            reverse_lazy('user-create'),
            follow=True,
            data={
                'first_name': 'Ivan',
                'last_name': 'Ivanov',
                'username': "ivan",
                "password1": "111",
                "password2": "111",
            },
        )
        self.assertRedirects(response, reverse_lazy('login'))
        self.assertIn(
            'User registered successfully',
            response.content.decode(),
        )
        self.assertTrue(
            self.users.filter(
                username='ivan', last_name='Ivanov', first_name='Ivan',
            ).exists(),
        )

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
        self.assertIn(
            'A user with that username already exists.',
            response.content.decode(),
        )
        self.assertTrue(
            self.users.filter(
                username='123', first_name='123', last_name='123',
            ).exists(),
        )

    def test_updated(self):
        response = self.client.post(
            reverse_lazy('user-update', kwargs={'pk': self.user.pk}),
            follow=True,
            data={
                'first_name': 'Igor',
                'last_name': 'Ivanov',
                'username': "igor",
                "password1": "111",
                "password2": "111",
            },
        )

        self.assertIn('User changed successfully', response.content.decode())
        self.assertTrue(
            self.users.filter(
                username='igor', first_name='Igor', last_name='Ivanov',
            ).exists(),
        )

    def test_updated_error(self):
        user_err = self.users.exclude(pk=self.user.pk).first()

        response = self.client.post(
            reverse_lazy('user-update', kwargs={'pk': user_err.pk}),
            follow=True,
            data={
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'username': "igor",
                "password1": "111",
                "password2": "111",
            },
        )

        self.assertIn(
            'You do not have permission to change the user otherwise.',
            response.content.decode(),
        )
        self.assertFalse(self.users.filter(username='igor').exists())

    def test_deleted_if_used(self):

        response = self.client.post(
            reverse_lazy('user-delete', kwargs={'pk': self.user.pk}),
            follow=True,
        )

        self.assertIn(
            'Unable to delete user because he is in use',
            response.content.decode(),
        )
        self.assertTrue(
            self.users.filter(username=self.user.username).exists(),
        )

    def test_deleted_other_user(self):
        """Remove another user"""
        user_err = self.users.exclude(pk=self.user.pk).first()

        response = self.client.post(
            reverse_lazy('user-delete', kwargs={'pk': user_err.pk}),
            follow=True,
        )

        self.assertIn(
            'You do not have permission to change the user otherwise.',
            response.content.decode(),
        )
        self.assertTrue(self.users.filter(username=user_err.username).exists())
