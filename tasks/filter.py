

import django_filters
from django import forms
from django.contrib.auth.models import User

from labels.models import Labels
from statuses.models import Statuses
from tasks.models import Tasks
from user.models import CustomUser


def only_self(request):
    """Show only own tasks."""
    if request is None:
        return User.objects.all()
    return User.objects.filter(pk=request.user.pk)

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
    author = django_filters.ModelChoiceFilter(
        queryset=only_self,
        field_name='author',
        label='Только свои задачи',
        # widget=forms.CheckboxInput(),
    )

    class Meta:
        model = Tasks
        fields = ['status', 'executor', 'label',]
