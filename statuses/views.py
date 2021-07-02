"""Logic for home, creating and editing statuses."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls.base import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from statuses.models import Status
from utils.mixins import DeleteMixin


class StatusesListView(LoginRequiredMixin, ListView):
    """Statuses list view."""

    template_name = 'statuses.html'
    model = Status
    context_object_name = 'statuses'
    login_url = reverse_lazy('login')


class StatusesCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Create status."""

    template_name = 'create.html'
    model = Status
    fields = ['name']

    login_url = reverse_lazy('login')

    success_message = _('Status created successfully')
    success_url = reverse_lazy('statuses')


class StatusesUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update status."""

    template_name = 'update.html'
    fields = ['name']
    model = Status

    success_url = reverse_lazy('statuses')
    login_url = reverse_lazy('login')

    success_message = _('Status changed successfully')


class StatusesDeleteView(LoginRequiredMixin, DeleteMixin, DeleteView):
    """Delete status."""

    template_name = "delete.html"
    model = Status

    success_url = reverse_lazy('statuses')
    login_url = reverse_lazy('login')

    success_message = _('Status deleted successfully')
    error_message = _('Unable to delete status because it is in use')
