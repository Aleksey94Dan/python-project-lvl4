"""Description of forms for tasks."""

from django.forms import ModelForm, widgets
from django.utils.translation import gettext_lazy as _

from tasks.models import Tasks


class CreateTaskForm(ModelForm):
    """Tasks."""

    class Meta:
        model = Tasks
        fields = ['name', 'description', 'status', 'executor', 'labels']
        labels = {
            'name': _('Имя'),
            'description': _('Описание'),
            'status': _('Статус'),
            'executor': _('Испольнитель'),
            'labels': _('Метки'),
        }

        widgets = {
            'labels': widgets.SelectMultiple(),
        }


class UpdateTaskForm(CreateTaskForm):
    """Update task."""
