"""Description of forms for tasks."""


from django.forms import HiddenInput, ModelForm
from django.utils.translation import ugettext as _

from tasks.models import Tasks


class CreateTaskForm(ModelForm):
    """Tasks."""

    class Meta:
        model = Tasks
        fields = [
            'name',
            'description',
            'status',
            'executor',
            'author',
            'labels',
        ]
        labels = {
            'name': _('Name'),
            'description': _('Description'),
            'status': _('Status'),
            'executor': _('Executor'),
            'author': _('Author'),
            'labels': _('Labels'),
        }
        widgets = {'author': HiddenInput()}

    def __init__(self, user, *args, **kwargs):
        """Init."""
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['author'].initial = user


class UpdateTaskForm(CreateTaskForm):
    """Update task."""
