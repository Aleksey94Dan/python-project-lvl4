# """Testing user create."""

# from http import HTTPStatus

# from django.contrib.auth.models import User
# from django.test import Client, TestCase
# from django.urls import reverse_lazy
# from faker import Faker


# class SuccessRegistrationTest(TestCase):
#     """Test user registration."""

#     def setUp(self):
#         """Create a test database."""
#         self.client = Client()
#         self.faker = Faker()

#     def test(self):
#         """Send valid registration request."""
#         response = self.client.get(reverse_lazy('user-create'))
#         self.assertEqual(response.status_code, HTTPStatus.OK)
#         first_name = self.faker.first_name()
#         last_name = self.faker.last_name()
#         username = self.faker.user_name()
#         password1 = self.faker.password()
#         password2 = password1
#         response = self.client.post(
#             reverse_lazy('user-create'),
#             data={
#                 'first_name': first_name,
#                 'last_name': last_name,
#                 'username': username,
#                 'password1': password1,
#                 'password2': password2,
#             },
#         )
#         self.assertRedirects(response, reverse_lazy('login'))
#         self.assertTrue(User.objects.filter(username=username))
