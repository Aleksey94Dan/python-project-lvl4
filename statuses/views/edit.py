"""Logic for creating and editing statuses."""

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from statuses.forms import CreateStatusForm, UpdateStatusForm
from statuses.models import Statuses
from user.mixins import CustomRequiredMixin

STATUS_MESSAGES = {
    'succes_create': _('Статус успешно создан'),
    'succes_update': _('Статус успешно изменён'),
    'succes_delete': _('Статус успешно удален'),
}.get


class StatusesCreateView(CustomRequiredMixin, SuccessMessageMixin, CreateView):
    """Create status."""

    template_name = 'creates.html'
    success_message = STATUS_MESSAGES('succes_create')
    form_class = CreateStatusForm
    success_url = reverse_lazy('statuses')
    extra_context = {
        'header': 'Cоздать статус',
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
        'header': 'Изменение статуса',
        'button': 'Изменить',
    }
    success_url = reverse_lazy('statuses')
    login_url = reverse_lazy('login')


class StatusesDeleteView(CustomRequiredMixin, DeleteView):
    """Delete status."""

    template_name = "deleting.html"
    success_message = STATUS_MESSAGES('succes_delete')
    model = Statuses
    extra_context = {'header': 'Удаление статуса'}
    success_url = reverse_lazy('statuses')
    login_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        """Delete status and display message"""
        super().post(request, *args, **kwargs)
        message_error = self.success_message
        if message_error:
            messages.add_message(
                self.request,
                messages.SUCCESS,
                message_error,
            )
        return HttpResponseRedirect(self.success_url)
