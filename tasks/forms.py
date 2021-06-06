"""Description of forms for tasks."""


from django.forms import HiddenInput, ModelForm
from django.utils.translation import gettext as _

from tasks.models import Task


class CreateTaskForm(ModelForm):
    """Tasks."""

    class Meta:
        model = Task
        fields = [
            'name',
            'description',
            'status',
            'executor',
            'author',
            'labels',
        ]
        labels = {
            'name': _('Имя'),
            'description': _('Описание'),
            'status': _('Статус'),
            'executor': _('Исполнитель'),
            'author': _('Автор'),
            'labels': _('Метки'),
        }
        widgets = {'author': HiddenInput()}

    def __init__(self, user, *args, **kwargs):
        """Init."""
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['author'].initial = user


class UpdateTaskForm(CreateTaskForm):
    """Update task."""
