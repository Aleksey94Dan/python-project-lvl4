"""Logic for creating and editing tasks."""

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from tasks.forms import CreateTaskForm, UpdateTaskForm
from tasks.models import Tasks
from user.mixins import CustomRequiredMixin

TASKS_MESSAGES = {
    'succes_create': _('Task successfully created'),
    'succes_update': _('Task successfully updated'),
    'succes_delete': _('Task successfully deleted'),
    'error_delete': _('A task can only be deleted by its author'),
}.get


class TasksCreateView(CustomRequiredMixin, SuccessMessageMixin, CreateView):
    """Create tasks."""

    template_name = 'creates.html'
    success_message = TASKS_MESSAGES('succes_create')
    form_class = CreateTaskForm
    success_url = reverse_lazy('tasks')
    extra_context = {
        'header': _('Create task'),
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
        'header': _('Changing a task'),
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
    error_message = TASKS_MESSAGES('error_delete')
    model = Tasks
    extra_context = {'header': _('Deleting')}
    success_url = reverse_lazy('tasks')
    login_url = reverse_lazy('login')

    def delete(self, request, *args, **kwargs):
        """Delete tasks and display message."""
        task = self.get_object()
        if task.author.pk == request.user.pk:
            messages.add_message(
                request,
                messages.SUCCESS,
                self.success_message,
            )
            return super().delete(request, *args, **kwargs)
        messages.add_message(
            request,
            messages.ERROR,
            self.error_message,
        )
        return HttpResponseRedirect(self.success_url)
