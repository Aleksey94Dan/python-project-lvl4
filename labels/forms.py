"""Description of forms for labels."""

from django.forms import ModelForm, TextInput
from django.utils.translation import ugettext as _

from labels.models import Labels


class CreateLabelForm(ModelForm):
    """Labels."""

    class Meta:
        model = Labels
        fields = ['name']
        labels = {'name': _('Name')}
        widgets = {'name': TextInput()}


class UpdateLabelForm(CreateLabelForm):
    """Update labels."""
