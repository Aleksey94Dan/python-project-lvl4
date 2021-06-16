"""Test user views."""


from django.test import TestCase, Client
from http import HTTPStatus
from django.urls import reverse_lazy

from seed.factories import UserFactory

class UserViewsTests(TestCase):

    def setUp(self):
        self.url = reverse_lazy('users-list')
        self.client = Client()

    # def test_user_list(self):
    #     users = UserFactory.create_batch(5)
    #     response = self.client.get(self.url)
    #     response_body = response.content.decode()

    #     self.assertEqual(response.status_code, HTTPStatus.OK)
    #     for user in users:
    #         self.assertInHTML(user.get_full_name(), response_body)


    def test_user_registration(self):
        users = UserFactory.create_batch(5)
        user_create = reverse_lazy('user-create')
        response = self.client.get(user_create)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        for user in users:
            data={
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'username': user.username,
                    'password1': user.password,
                    'password2': user.password,
                }
            response = self.client.post(
                user_create,
                data=data,
            )
            self.assertRedirects(response, reverse_lazy('login'))