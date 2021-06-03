"""Logic for creating and editing statuses."""

from django.contrib.messages.views import SuccessMessageMixin
from django.urls.base import reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic.edit import CreateView, UpdateView

from statuses.forms import CreateStatusForm, UpdateStatusForm
from statuses.models import Statuses
from user.messages import STATUS_MESSAGES
from user.mixins import CustomDeleteViewMixin, CustomRequiredMixin


class StatusesCreateView(CustomRequiredMixin, SuccessMessageMixin, CreateView):
    """Create status."""

    template_name = 'creates.html'
    success_message = STATUS_MESSAGES('succes_create')
    form_class = CreateStatusForm
    success_url = reverse_lazy('statuses')
    extra_context = {
        'header': _('Create status'),
        'button': 'Создать',
    }
    login_url = reverse_lazy('login')


class StatusesUpdateView(CustomRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update status."""

    template_name = 'creates.html'
    success_message = STATUS_MESSAGES('succes_update')
    form_class = UpdateStatusForm
    model = Statuses
    extra_context = {
        'header': _('Update status'),
        'button': 'Изменить',
    }
    success_url = reverse_lazy('statuses')
    login_url = reverse_lazy('login')


class StatusesDeleteView(CustomDeleteViewMixin):
    """Delete status."""

    template_name = "deleting.html"
    success_message = STATUS_MESSAGES('succes_delete')
    error_message = STATUS_MESSAGES('error_delete')
    model = Statuses
    extra_context = {'header': _('Deleting status')}
    success_url = reverse_lazy('statuses')
    login_url = reverse_lazy('login')
