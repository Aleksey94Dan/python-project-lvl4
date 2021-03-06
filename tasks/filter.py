from django import forms
from django.utils.translation import gettext_lazy as _

import django_filters  # noqa: I001
from labels.models import Label
from statuses.models import Status
from tasks.models import Task
from user.models import User


class TaskFilter(django_filters.FilterSet):
    """Filter for sorting jobs."""

    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        field_name='status',
        label=_('Status'),
    )
    label = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        field_name='labels',
        label=_('Label'),
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        field_name='executor',
        label=_('Executor'),
    )
    only_self = django_filters.BooleanFilter(
        method='filter_by_self',
        label=_('Only your tasks'),
        widget=forms.CheckboxInput(),
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label']

    def filter_by_self(self, queryset, name, value):  # noqa: WPS110
        """Return only your tasks."""
        if value:
            return queryset.filter(author=self.request.user.pk)
        return queryset
