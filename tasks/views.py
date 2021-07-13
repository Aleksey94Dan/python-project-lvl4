"""Logic for home, creating and editing tasks."""


from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django_filters.views import FilterView  # noqa: I001

from task_manager.mixins import TaskDeleteMixin
from tasks.filter import TaskFilter
from tasks.forms import TaskForm
from tasks.models import Task


class TasksListView(LoginRequiredMixin, FilterView):
    """Tasks list view."""

    template_name = 'tasks.html'
    login_url = reverse_lazy('login')
    filterset_class = TaskFilter


class TasksTicketView(DetailView):
    """Detail task."""

    template_name = 'task_ticket.html'
    model = Task
    context_object_name = 'task'


class TasksCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Create tasks."""

    template_name = 'create.html'
    success_message = _('Task successfully created')
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        """Add author to form."""
        form.instance.author = self.request.user
        return super().form_valid(form)


class TasksUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update tasks."""

    template_name = 'update.html'
    success_message = _('Task successfully changed')
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    login_url = reverse_lazy('login')
    model = Task


class TasksDeleteView(LoginRequiredMixin, TaskDeleteMixin, DeleteView):
    """Delete tasks."""

    template_name = "delete.html"
    success_message = _('Task successfully deleted')
    error_message = _('A task can only be deleted by its author')
    model = Task
    success_url = reverse_lazy('tasks')
    login_url = reverse_lazy('login')
