"""Logic for home page of tasks"""

from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from tasks.filter import TaskFilter
from tasks.models import Task
from user.mixins import CustomRequiredMixin


class TasksListView(CustomRequiredMixin, ListView):
    """Tasks list view."""

    template_name = 'tasks.html'
    model = Task
    login_url = reverse_lazy('login')
    queryset = Task.objects.all()

    def get_context_data(self, *args, **kwargs):
        """Pass filter to context."""
        context = super().get_context_data(*args, **kwargs)
        context['filter'] = TaskFilter(
            data=self.request.GET or None,
            request=self.request,
            queryset=self.queryset,
        )
        return context


class TasksTicketView(CustomRequiredMixin, DetailView):
    """Detail task."""

    template_name = 'task_ticket.html'
    model = Task
    context_object_name = 'task'
    extra_context = {'header': _('View a task')}

    def get_object(self):
        """Return object for detail."""
        id_ = self.kwargs.get("id")
        return get_object_or_404(self.model, id=id_)
