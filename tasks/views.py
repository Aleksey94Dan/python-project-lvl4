"""Logic for home, creating and editing tasks."""


from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from django_filters.views import FilterView  # noqa: I001
from tasks.filter import TaskFilter
from tasks.forms import TaskForm
from tasks.models import Task
from user.mixins import CustomRequiredMixin


class TasksListView(CustomRequiredMixin, FilterView):
    """Tasks list view."""

    template_name = 'tasks.html'
    login_url = reverse_lazy('login')
    filterset_class = TaskFilter


class TasksTicketView(CustomRequiredMixin, DetailView):
    """Detail task."""

    template_name = 'task_ticket.html'
    model = Task
    context_object_name = 'task'


class TasksCreateView(CustomRequiredMixin, SuccessMessageMixin, CreateView):
    """Create tasks."""

    template_name = 'creates.html'
    success_message = _('Задача успешно создана')
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        """Add author to form."""
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class TasksUpdateView(CustomRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update tasks."""

    template_name = 'updates.html'
    success_message = _('Задача успешно изменена')
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    login_url = reverse_lazy('login')
    model = Task


class TasksDeleteView(CustomRequiredMixin, DeleteView):
    """Delete tasks."""

    template_name = "removes.html"
    success_message = _('Задача успешно удалена')
    error_message = _('Задачу может удалить только её автор')
    model = Task
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
