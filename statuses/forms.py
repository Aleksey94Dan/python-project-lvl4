"""Description of forms for status."""

from django.forms import ModelForm, TextInput
from django.utils.translation import gettext as _

from statuses.models import Status


class CreateStatusForm(ModelForm):
    """Statuses."""

    class Meta:
        model = Status
        fields = ['name']
        labels = {'name': _('Имя')}
        widgets = {'name': TextInput()}


class UpdateStatusForm(CreateStatusForm):
    """Update statuses."""
