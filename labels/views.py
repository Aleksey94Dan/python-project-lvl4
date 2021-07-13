"""Logic for home, creating and editing labels."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from labels.models import Label
from task_manager.mixins import DeleteMixin


class LabelsListView(LoginRequiredMixin, ListView):
    """Labels list view."""

    template_name = 'labels.html'
    model = Label
    context_object_name = 'labels'
    login_url = reverse_lazy('login')


class LabelsCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Create status."""

    template_name = 'create.html'
    success_message = _('Label created successfully')
    fields = ['name']
    model = Label
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('labels')


class LabelsUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update status."""

    template_name = 'update.html'
    success_message = _('Label updated successfully')
    fields = ['name']
    model = Label
    success_url = reverse_lazy('labels')
    login_url = reverse_lazy('login')


class LabelsDeleteView(LoginRequiredMixin, DeleteMixin, DeleteView):
    """Delete status."""

    template_name = "delete.html"
    success_message_delete = _('Label deleted successfully')
    error_message_delete = _('Cannot remove a label because it is in use')
    model = Label
    success_url = reverse_lazy('labels')
    login_url = reverse_lazy('login')
