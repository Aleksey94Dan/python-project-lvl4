"""Модели описания для task"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    """Модель обозначения статуса"""
    name = models.CharField(_("name of status"), max_length=100)
    date_joined = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Label(models.Model):
    """Модель обозначения метки"""
    name = models.CharField(_("name of label"), max_length=100)
    date_joined = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    """Модель обозначения задачи"""

    name = models.CharField(_("name of task"), max_length=100)
    date_joined = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
