"""Logic for home, creating and editing tasks."""

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django_filters.views import FilterView  # noqa: I001

from task_manager.mixins import AuthRequiredMixin, DeleteMixin
from tasks.filter import TaskFilter
from tasks.forms import TaskForm
from tasks.mixins import TaskTestAccountMixin
from tasks.models import Task


class TasksListView(AuthRequiredMixin, FilterView):
    """Tasks list view."""

    template_name = 'tasks.html'
    filterset_class = TaskFilter
    model = Task
    ordering = ['-pk']


class TasksTicketView(AuthRequiredMixin, DetailView):
    """Detail task."""

    template_name = 'task_ticket.html'
    model = Task
    context_object_name = 'task'


class TasksCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    """Create tasks."""

    template_name = 'create.html'
    success_message = _('Task successfully created')
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    model = Task

    def form_valid(self, form):
        """Add author to form."""
        form.instance.author = self.request.user
        return super().form_valid(form)


class TasksUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update tasks."""

    template_name = 'update.html'
    success_message = _('Task successfully changed')
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    model = Task


class TasksDeleteView(  # noqa: WPS215
    AuthRequiredMixin,
    TaskTestAccountMixin,
    DeleteMixin,
    DeleteView,
):
    """Delete tasks."""

    template_name = "delete.html"
    success_message_delete = _('Task successfully deleted')
    model = Task
    success_url = reverse_lazy('tasks')
