

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """User mediator model."""

    def __str__(self):  # noqa: D105
        return self.get_full_name()
