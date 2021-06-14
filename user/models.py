

from django.contrib.auth.models import User


class CustomUser(User):
    """User mediator model."""

    class Meta:
        proxy = True

    def __str__(self):  # noqa: D105
        return self.get_full_name()
