"""Description of status models."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Statuses(models.Model):
    """Status designation model."""

    name = models.CharField(_("name of status"), max_length=100)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):  # noqa: D105
        return self.name
