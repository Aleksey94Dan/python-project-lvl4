"""Logic for home, creating and editing labels."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from labels.models import Label


class LabelsListView(LoginRequiredMixin, ListView):
    """Labels list view."""

    template_name = 'labels.html'
    model = Label
    context_object_name = 'labels'
    login_url = reverse_lazy('login')


class LabelsCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Create label."""

    template_name = 'create.html'
    success_message = _('Label created successfully')
    fields = ['name']
    model = Label
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('labels')


class LabelsUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update label."""

    template_name = 'update.html'
    success_message = _('Label updated successfully')
    fields = ['name']
    model = Label
    success_url = reverse_lazy('labels')
    login_url = reverse_lazy('login')


class LabelsDeleteView(LoginRequiredMixin, DeleteView):
    """Delete labels."""

    template_name = "delete.html"
    model = Label
    success_url = reverse_lazy('labels')
    login_url = reverse_lazy('login')

    def delete(self, request, *args, **kwargs):  # noqa: D102
        if self.get_object().task_set.exists():
            messages.add_message(
                request,
                messages.ERROR,
                _('Cannot remove a label because it is in use'),
            )
            return HttpResponseRedirect(self.success_url)
        messages.add_message(
            request,
            messages.SUCCESS,
            _('Label deleted successfully'),
        )
        return super().delete(request, *args, **kwargs)
