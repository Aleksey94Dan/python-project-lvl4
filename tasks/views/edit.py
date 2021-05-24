"""Logic for creating and editing tasks."""

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db import models
from django.http import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from tasks.forms import CreateTaskForm, UpdateTaskForm
from tasks.models import Tasks
from user.mixins import CustomRequiredMixin

TASKS_MESSAGES = {
    'succes_create': _('Задача успешно создан'),
    'succes_update': _('Задача успешно изменён'),
    'succes_delete': _('Задача успешно удален'),
}.get


class TasksCreateView(CustomRequiredMixin, SuccessMessageMixin, CreateView):
    """Create tasks."""

    template_name = 'creates.html'
    success_message = TASKS_MESSAGES('succes_create')
    form_class = CreateTaskForm
    success_url = reverse_lazy('tasks')
    extra_context = {
        'header': 'Cоздать задачу',
        'button': 'Создать',
    }
    login_url = reverse_lazy('login')
    model = Tasks


    def get_form_kwargs(self, *args, **kwargs):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs


class TasksUpdateView(CustomRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update tasks."""

    template_name = 'creates.html'
    success_message = TASKS_MESSAGES('succes_update')
    form_class = UpdateTaskForm
    model = Tasks
    extra_context = {
        'header': 'Изменение задачи',
        'button': 'Изменить',
    }
    success_url = reverse_lazy('tasks')
    login_url = reverse_lazy('login')

    def get_form_kwargs(self, *args, **kwargs):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs


class TasksDeleteView(CustomRequiredMixin, DeleteView):
    """Delete tasks."""

    template_name = "deleting.html"
    success_message = TASKS_MESSAGES('succes_delete')
    model = Tasks
    extra_context = {'header': 'Удаление '}
    success_url = reverse_lazy('tasks')
    login_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        """Delete tasks and display message"""
        super().post(request, *args, **kwargs)
        message_error = self.success_message
        if message_error:
            messages.add_message(
                self.request,
                messages.SUCCESS,
                message_error,
            )
        return HttpResponseRedirect(self.success_url)
