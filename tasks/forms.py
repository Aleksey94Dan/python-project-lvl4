"""Description of forms for tasks."""


from django.forms import HiddenInput, ModelForm, ModelMultipleChoiceField
from django.utils.translation import gettext_lazy as _

from labels.models import Labels
from tasks.models import Tasks


class CreateTaskForm(ModelForm):
    """Tasks."""

    labels = ModelMultipleChoiceField(
        queryset=Labels.objects.all(),
        label=_('Метки'),
    )

    class Meta:
        model = Tasks
        fields = ['name', 'description', 'status', 'executor', 'author']
        labels = {
            'name': _('Имя'),
            'description': _('Описание'),
            'status': _('Статус'),
            'executor': _('Испольнитель'),
            'author': _('Автор'),
        }
        widgets = {
            'author': HiddenInput(),
        }

    def __init__(self, user, *args, **kwargs):
        """Init."""
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['author'].initial = user


class UpdateTaskForm(CreateTaskForm):
    """Update task."""
