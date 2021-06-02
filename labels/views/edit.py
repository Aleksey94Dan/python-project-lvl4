"""Logic for creating and editing labels."""

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls.base import reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic.edit import CreateView, UpdateView

from labels.forms import CreateLabelForm, UpdateLabelForm
from labels.models import Labels
from user.messages import LABEL_MESSAGES
from user.mixins import CustomDeleteViewMixin, CustomRequiredMixin


class LabelsCreateView(CustomRequiredMixin, SuccessMessageMixin, CreateView):
    """Create status."""

    template_name = 'creates.html'
    success_message = LABEL_MESSAGES('succes_create')
    form_class = CreateLabelForm
    success_url = reverse_lazy('labels')
    extra_context = {
        'header': _('Create a label'),
        'button': 'Создать',
    }
    login_url = reverse_lazy('login')


class LabelsUpdateView(CustomRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update status."""

    template_name = 'creates.html'
    success_message = LABEL_MESSAGES('succes_update')
    form_class = UpdateLabelForm
    model = Labels
    extra_context = {
        'header': _('Change label'),
        'button': 'Изменить',
    }
    success_url = reverse_lazy('labels')
    login_url = reverse_lazy('login')


class LabelsDeleteView(CustomRequiredMixin, CustomDeleteViewMixin):
    """Delete status."""

    template_name = "deleting.html"
    success_message = LABEL_MESSAGES('succes_delete')
    error_message = LABEL_MESSAGES('error_delete')
    model = Labels
    extra_context = {'header': _('Delete label')}
    success_url = reverse_lazy('labels')
    login_url = reverse_lazy('login')
