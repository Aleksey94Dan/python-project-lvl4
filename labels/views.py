"""Logic for home, creating and editing labels."""

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from labels.forms import LabelForm
from labels.models import Label
from user.mixins import CustomDeleteMixin, CustomRequiredMixin


class LabelsListView(CustomRequiredMixin, ListView):
    """Labels list view."""

    template_name = 'labels.html'
    model = Label
    context_object_name = 'labels'
    login_url = reverse_lazy('login')


class LabelsCreateView(CustomRequiredMixin, SuccessMessageMixin, CreateView):
    """Create status."""

    template_name = 'creates.html'
    success_message = _('Метка успешно создана')
    form_class = LabelForm
    model = Label
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('labels')


class LabelsUpdateView(CustomRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update status."""

    template_name = 'updates.html'
    success_message = _('Метка успешно изменена')
    form_class = LabelForm
    model = Label
    success_url = reverse_lazy('labels')
    login_url = reverse_lazy('login')


class LabelsDeleteView(CustomDeleteMixin, DeleteView):
    """Delete status."""

    template_name = "removes.html"
    success_message = _('Метка успешно удалена')
    error_message = _('Невозможно удалить метку, потому что она используется')
    model = Label
    success_url = reverse_lazy('labels')
    login_url = reverse_lazy('login')
