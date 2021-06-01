"""Logic for creating and editing statuses."""

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from statuses.forms import CreateStatusForm, UpdateStatusForm
from statuses.models import Statuses
from user.mixins import CustomRequiredMixin

STATUS_MESSAGES = {
    'succes_create': _('Status successfully created'),
    'succes_update': _('Status successfully updated'),
    'succes_delete': _('Status successfully deleted'),
    'error_delete': _('Unable to delete status because it is in use'),
}.get


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


class StatusesDeleteView(CustomRequiredMixin, DeleteView):
    """Delete status."""

    template_name = "deleting.html"
    success_message = STATUS_MESSAGES('succes_delete')
    error_message = STATUS_MESSAGES('error_delete')
    model = Statuses
    extra_context = {'header': _('Deleting status')}
    success_url = reverse_lazy('statuses')
    login_url = reverse_lazy('login')

    def delete(self, request, *args, **kwargs):
        """Delete status and display message"""
        status = self.get_object()
        related_tasks = status.has_related()

        if related_tasks:
            messages.add_message(
                request,
                messages.ERROR,
                self.error_message,
            )
            return HttpResponseRedirect(self.success_url)
        messages.add_message(
            request,
            messages.SUCCESS,
            self.success_message,
        )
        return super().delete(request, *args, **kwargs)
