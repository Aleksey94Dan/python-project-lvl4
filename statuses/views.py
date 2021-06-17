"""Logic for home, creating and editing statuses."""

from django.contrib.messages.views import SuccessMessageMixin
from django.urls.base import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from statuses.forms import StatusForm
from statuses.models import Status
from user.mixins import CustomDeleteMixin, CustomRequiredMixin


class StatusesListView(CustomRequiredMixin, ListView):
    """Statuses list view."""

    template_name = 'statuses.html'
    model = Status
    context_object_name = 'statuses'
    login_url = reverse_lazy('login')


class StatusesCreateView(CustomRequiredMixin, SuccessMessageMixin, CreateView):
    """Create status."""

    template_name = 'creates.html'
    success_message = _('Статус успешно создан')
    form_class = StatusForm
    success_url = reverse_lazy('statuses')
    login_url = reverse_lazy('login')


class StatusesUpdateView(CustomRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update status."""

    template_name = 'updates.html'
    success_message = _('Статус успешно изменён')
    form_class = StatusForm
    model = Status
    success_url = reverse_lazy('statuses')
    login_url = reverse_lazy('login')


class StatusesDeleteView(CustomRequiredMixin, CustomDeleteMixin, DeleteView):
    """Delete status."""

    template_name = "removes.html"
    success_message = _('Статус успешно удалён')
    error_message = _('Невозможно удалить статус, потому что он используется')
    model = Status
    success_url = reverse_lazy('statuses')
    login_url = reverse_lazy('login')
