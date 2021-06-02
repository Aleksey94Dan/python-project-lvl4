"""Logic for creating and editing labels."""

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from labels.forms import CreateLabelForm, UpdateLabelForm
from labels.models import Labels
from user.mixins import CustomRequiredMixin

LABEL_MESSAGES = {
    'succes_create': _('Label created successfully'),
    'succes_update': _('Label changed successfully'),
    'succes_delete': _('Label deleted successfully'),
    'error_delete': _('Cannot remove a label because it is in use'),
}.get


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
        'header': 'Change label',
        'button': 'Изменить',
    }
    success_url = reverse_lazy('labels')
    login_url = reverse_lazy('login')


class LabelsDeleteView(CustomRequiredMixin, DeleteView):
    """Delete status."""

    template_name = "deleting.html"
    success_message = LABEL_MESSAGES('succes_delete')
    error_message = LABEL_MESSAGES('error_delete')
    model = Labels
    extra_context = {'header': 'Удалить метку'}
    success_url = reverse_lazy('labels')
    login_url = reverse_lazy('login')

    def delete(self, request, *args, **kwargs):
        """Delete status and display message."""
        label = self.get_object()
        related_tasks = label.has_related()

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
