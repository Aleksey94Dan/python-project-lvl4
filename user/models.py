

from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    """User mediator model."""

    def __str__(self):  # noqa: D105
        return self.get_full_name()

    def get_absolute_url(self):
        return reverse('users-list')
