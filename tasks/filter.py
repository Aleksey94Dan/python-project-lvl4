

import django_filters

from labels.models import Labels
from statuses.models import Statuses
from tasks.models import Tasks
from user.models import CustomUser

CHOICES = (('1', '1'),)


class TaskFilter(django_filters.FilterSet):
    """Filter for sorting jobs."""

    status = django_filters.ModelChoiceFilter(
        queryset=Statuses.objects.all(),
        field_name='status',
        label='Статус',
    )
    label = django_filters.ModelChoiceFilter(
        queryset=Labels.objects.all(),
        field_name='labels',
        label='Метки',
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=CustomUser.objects.all(),
        field_name='executor',
        label='Исполнитель',
    )

    only_self = django_filters.ChoiceFilter(
        choices=CHOICES,
        method='filter_by_self',
        label='Только свои задачи',
    )

    class Meta:
        model = Tasks
        fields = ['status', 'executor', 'label']

    def filter_by_self(self, queryset, name, value):  # noqa: WPS110
        """Return only your tasks."""
        if value:
            return queryset.filter(author=self.request.user.pk)
        return queryset.all()
