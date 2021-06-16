# """Testing user delete."""

# from http import HTTPStatus

# from django.contrib.auth.models import User
# from django.test import Client, TestCase
# from django.urls import reverse_lazy


# class TestUserDeleteView(TestCase):
#     """Test deleted view."""

#     def setUp(self):
#         """Create a test database."""
#         self.user = User.objects.create(username='testuser')
#         self.user.set_password('12345')
#         self.user.save()
#         self.url = reverse_lazy('user-delete', kwargs={'pk': self.user.pk})
#         self.client = Client()

#     def test_delete_not_logged_in(self):
#         """Testing user delete if not logged in."""
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, HTTPStatus.FOUND)
#         response = self.client.post(self.url)
#         self.assertRedirects(response, reverse_lazy('login'))

#     def test_delete_logged_in(self):
#         """Testing user delete if logged in."""
#         response = self.client.get(reverse_lazy('login'))
#         self.assertEqual(response.status_code, HTTPStatus.OK)
#         response = self.client.post(
#             reverse_lazy('login'),
#             data={
#                 'username': 'testuser',
#                 'password': '12345',
#             },
#         )
#         self.assertRedirects(response, reverse_lazy('home'))
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, HTTPStatus.OK)
#         response = self.client.post(self.url)
#         self.assertRedirects(response, reverse_lazy('users-list'))
