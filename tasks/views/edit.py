"""Logic for creating and editing statuses."""

from django.contrib.messages.views import SuccessMessageMixin
from django.urls.base import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from tasks.forms import CreateStatusForm, UpdateStatusForm
from tasks.models.models import Statuses


class StatusesCreateView(SuccessMessageMixin, CreateView):
    """Create status."""

    template_name = 'creates.html'
    success_message = _("Статус успешно создан")
    form_class = CreateStatusForm
    success_url = reverse_lazy('statuses')
    extra_context = {
        'header': 'Cоздать статус',
        'button': 'Создать',
    }


class StatusesUpdateView(SuccessMessageMixin, UpdateView):
    """Update status."""

    template_name = 'creates.html'
    success_message = _("Статус успешно изменён")
    form_class = UpdateStatusForm
    model = Statuses
    extra_context = {
        'header': 'Изменение статуса',
        'button': 'Изменить',
    }
    success_url = reverse_lazy('statuses')


class StatusesDeleteView(SuccessMessageMixin, DeleteView):
    """Delete status."""

    template_name = "deleting.html"
    success_message = _("Статус успешно удален")
    model = Statuses
    extra_context = {'header': 'Удаление статуса'}
    success_url = reverse_lazy('statuses')
