"""Description of tasks models."""

from django.db import models
from django.utils.translation import ugettext as _

from labels.models import Label
from statuses.models import Status
from user.models import CustomUser


class Task(models.Model):
    """Status designation model."""

    name = models.CharField(_("name of task"), max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    author = models.ForeignKey(
        CustomUser,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        related_name='description',
        null=True,
        blank=False,
    )
    labels = models.ManyToManyField(
        Label,
        blank=True,
    )
    executor = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='executor',
        blank=True,
        null=True,
    )

    def __str__(self):  # noqa: D105
        return self.name
