"""Description of forms for tasks."""

from django import forms
from django.forms import ModelForm, widgets
from django.utils.translation import gettext_lazy as _

from labels.models import Labels
from statuses.models import Statuses
from tasks.models import Tasks


BLANK_CHOICE = [('', '-----')]

class TaskListSortForm(forms.Form):
    """A form for sort and search."""

    status = forms.ChoiceField(label=_("Статус"), required=False)
    executor = forms.ChoiceField(label=_("Исполнитель"), required=False)
    labels = forms.ChoiceField(label=_("Метка"), required=False)
    only_myself = forms.BooleanField(
        label=_("Только свои задачи"),
        required=False,
        initial=False,
    )

    def __init__(self, statuses, labels, executor, *args, **kwargs):
        """Initialize the form."""
        self.statuses = statuses
        self.labels = labels
        self.executor = executor
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = BLANK_CHOICE + [
            (status.pk, status.name) for status in statuses
        ]
        self.fields['labels'].choices = BLANK_CHOICE + [
            (label.pk, label.name) for label in labels
        ]
        self.fields['executor'].choices = BLANK_CHOICE + [
            (ex.pk, ex.get_full_name()) for ex in executor
        ]

class CreateTaskForm(ModelForm):
    """Tasks."""

    labels = forms.ModelMultipleChoiceField(queryset=Labels.objects.all())

    class Meta:
        model = Tasks
        fields = ['name', 'description', 'status', 'executor', 'author']
        labels = {
            'name': _('Имя'),
            'description': _('Описание'),
            'status': _('Статус'),
            'executor': _('Испольнитель'),
            'author': _('Автор')
        }
        widgets = {
            'author': forms.HiddenInput(),
        }

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CreateTaskForm, self).__init__(*args, **kwargs)
        self.fields['author'].initial = user
        self['labels'].label = _('Метки')


class UpdateTaskForm(CreateTaskForm):
    """Update task."""
