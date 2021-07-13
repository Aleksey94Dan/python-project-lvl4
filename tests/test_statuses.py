"""Test views"""

from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from user.models import User


class TestUserView(TestCase):
    """CRUD tests"""

    fixtures = ['statuses.json']

    @classmethod
    def setUpTestData(cls):
        """User initialization."""
        cls.User = get_user_model()