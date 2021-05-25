"""Description of forms for tasks."""

from django.forms import ModelForm, widgets
from django import forms
from django.utils.translation import gettext_lazy as _

from tasks.models import Tasks
from labels.models import Labels


class TaskListSortForm(forms.Form):
    """A form for sort and search."""

    status = forms.ChoiceField(label=_("Статус"), required=False)
    executor = forms.ChoiceField(label=_("Исполнитель"), required=False)
    labels = forms.ChoiceField(label=_("Метка"), required=False)
    their_tasks = forms.BooleanField(
        label=_("Только свои задачи"),
        required=False,
        initial=False,
    )

    def __init__(self, *args, **kwargs):
        """Initialize the form."""
        super().__init__(*args, **kwargs)


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



