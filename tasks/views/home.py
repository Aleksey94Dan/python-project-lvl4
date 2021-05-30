"""Logic for home page of tasks"""

from django.urls import reverse_lazy
from django.views.generic.list import ListView

from tasks.filter import TaskFilter
from tasks.models import Tasks
from user.mixins import CustomRequiredMixin


class TasksListView(ListView):
    """Tasks list view."""

    template_name = 'tasks.html'
    model = Tasks
    login_url = reverse_lazy('login')


    def get_context_data(self, *args, **kwargs):
        """Pass filter to context."""
        context = super().get_context_data(*args, **kwargs)
        context['filter'] = TaskFilter(
            data=self.request.GET,
            request=self.request,
            queryset=self.queryset,
        )
        return context
