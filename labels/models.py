"""Description of labels models."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    """Status designation model."""

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=100,
        unique=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # noqa: D105
        return self.name
