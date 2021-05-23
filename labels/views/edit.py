"""Logic for creating and editing labels."""

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from labels.forms import CreateLabelForm, UpdateLabelForm
from labels.models import Labels
from user.mixins import CustomRequiredMixin

LABEL_MESSAGES = {
    'succes_create': _('Метка успешно создана'),
    'succes_update': _('Метка успешно изменена'),
    'succes_delete': _('Метка успешно удалена'),
}.get


class LabelsCreateView(CustomRequiredMixin, SuccessMessageMixin, CreateView):
    """Create status."""

    template_name = 'creates.html'
    success_message = LABEL_MESSAGES('succes_create')
    form_class = CreateLabelForm
    success_url = reverse_lazy('labels')
    extra_context = {
        'header': 'Cоздать метку',
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
        'header': 'Изменить метку',
        'button': 'Изменить',
    }
    success_url = reverse_lazy('labels')
    login_url = reverse_lazy('login')


class LabelsDeleteView(CustomRequiredMixin, DeleteView):
    """Delete status."""

    template_name = "deleting.html"
    success_message = LABEL_MESSAGES('succes_delete')
    model = Labels
    extra_context = {'header': 'Удалить метку'}
    success_url = reverse_lazy('labels')
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
