"""Description of tasks models."""

from django.db import models
from django.utils.translation import gettext as _

from labels.models import Label
from statuses.models import Status
from user.models import CustomUser


class Task(models.Model):
    """Status designation model."""

    name = models.CharField(verbose_name=_('Имя'), max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    description = models.TextField(verbose_name=_('Описание'), blank=True)
    author = models.ForeignKey(
        CustomUser,
        verbose_name=_('Автор'),
        blank=True,
        null=False,
        on_delete=models.CASCADE,
    )
    status = models.ForeignKey(
        Status,
        verbose_name=_('Статус'),
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )
    executor = models.ForeignKey(
        CustomUser,
        verbose_name=_('Исполнитель'),
        on_delete=models.SET_NULL,
        related_name='executor',
        blank=True,
        null=True,
    )
    labels = models.ManyToManyField(
        Label,
        verbose_name=_('Метки'),
        blank=True,
    )

    def __str__(self):  # noqa: D105
        return self.name
