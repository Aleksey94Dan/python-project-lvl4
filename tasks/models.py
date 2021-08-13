"""Description of tasks models."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from labels.models import Label
from statuses.models import Status
from user.models import User


class Task(models.Model):
    """Status designation model."""

    name = models.CharField(
        verbose_name=_('Name'),
        max_length=100,
        unique=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(verbose_name=_('Description'), blank=True)
    author = models.ForeignKey(
        User,
        verbose_name=_('Author'),
        on_delete=models.PROTECT,
    )
    status = models.ForeignKey(
        Status,
        verbose_name=_('Status'),
        on_delete=models.PROTECT,
        null=True,
    )
    executor = models.ForeignKey(
        User,
        verbose_name=_('Executor'),
        on_delete=models.PROTECT,
        related_name='tasks',
        blank=True,
        null=True,
    )
    labels = models.ManyToManyField(
        Label,
        verbose_name=_('Labels'),
        blank=True,
    )

    def __str__(self):  # noqa: D105
        return self.name
