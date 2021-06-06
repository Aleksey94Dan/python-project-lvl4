

import django_filters
from django import forms
from django.utils.translation import gettext as _

from labels.models import Label
from statuses.models import Status
from tasks.models import Task
from user.models import CustomUser

CHOICES = (('1', ''),)


class TaskFilter(django_filters.FilterSet):
    """Filter for sorting jobs."""

    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        field_name='status',
        label=_('Статус'),
    )
    label = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        field_name='labels',
        label=_('Метки'),
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=CustomUser.objects.all(),
        field_name='executor',
        label=_('Исполнитель'),
    )

    only_self = django_filters.MultipleChoiceFilter(
        choices=CHOICES,
        method='filter_by_self',
        label=_('Только свои задачи'),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label']

    def filter_by_self(self, queryset, name, value):  # noqa: WPS110
        """Return only your tasks."""
        if value:
            return queryset.filter(author=self.request.user.pk)
        return queryset.all()
