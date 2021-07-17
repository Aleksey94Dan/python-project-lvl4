"""Description of labels models."""

from django.db import IntegrityError, models
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    """Status designation model."""

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=100,
        unique=True,
    )
    created_at = models.DateTimeField(auto_now=True)

    def delete(self, *args, **kwargs):
        """Raise an exception when deleting a dependent object."""
        if self.task_set.exists():
            raise IntegrityError
        return super().delete(*args, **kwargs)

    def __str__(self):  # noqa: D105
        return self.name
