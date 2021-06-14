"""Description of forms for labels."""

from django.forms import ModelForm, TextInput
from django.utils.translation import gettext as _

from labels.models import Label


class LabelForm(ModelForm):
    """Labels."""

    class Meta:
        model = Label
        fields = ['name']
        labels = {'name': _('Имя')}
        widgets = {'name': TextInput()}
