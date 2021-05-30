"""Description of tasks models."""

from django.db import models
from django.db.models.deletion import SET_NULL
from django.utils.translation import gettext_lazy as _

from labels.models import Labels
from statuses.models import Statuses
from user.models import CustomUser


class Tasks(models.Model):
    """Status designation model."""

    name = models.CharField(_("name of task"), max_length=100)
    created_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    author = models.ForeignKey(
        CustomUser,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    status = models.ForeignKey(
        Statuses,
        on_delete=SET_NULL,
        related_name='description',
        null=True,
        blank=False,
    )
    labels = models.ForeignKey(
        Labels,
        on_delete=SET_NULL,
        related_name='labels',
        blank=False,
        null=True,
        default='',
    )
    executor = models.ForeignKey(
        CustomUser,
        on_delete=SET_NULL,
        related_name='executor',
        blank=True,
        null=True,
    )

    def __str__(self):  # noqa: D105
        return self.name
