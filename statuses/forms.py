"""Description of forms for status."""

from django.forms import ModelForm, TextInput
from django.utils.translation import gettext as _

from statuses.models import Status


class StatusForm(ModelForm):
    """Statuses."""

    class Meta:
        model = Status
        fields = ['name']
        labels = {'name': _('Имя')}
        widgets = {'name': TextInput()}
