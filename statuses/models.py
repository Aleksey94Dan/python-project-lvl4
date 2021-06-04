"""Description of status models."""

from django.db import models
from django.utils.translation import ugettext as _


class Status(models.Model):
    """Status designation model."""

    name = models.CharField(_("name of status"), max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now=True)

    def has_related(self):
        """Is there a connection with tasks."""
        return self.description.exists()

    def __str__(self):  # noqa: D105
        return self.name
