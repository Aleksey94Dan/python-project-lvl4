"""Statuses, labels and tasks forms."""

from django.forms import ModelForm, TextInput
from django.utils.translation import gettext_lazy as _

from statuses.models import Statuses


class CreateStatusForm(ModelForm):
    """Statuses."""

    class Meta:
        model = Statuses
        fields = ['name']
        labels = {'name': _('Имя')}
        widgets = {'name': TextInput()}


class UpdateStatusForm(CreateStatusForm):
    """Update statuses."""
