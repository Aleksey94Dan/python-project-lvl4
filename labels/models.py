"""Description of labels models."""

from django.db import models
from django.utils.translation import ugettext as _


class Labels(models.Model):
    """Status designation model."""

    name = models.CharField(_("name of labels"), max_length=100)
    created_at = models.DateTimeField(auto_now=True)

    def has_related(self):
        """Is there a connection with tasks."""
        return self.tasks_set.exists()

    def __str__(self):  # noqa: D105
        return self.name
