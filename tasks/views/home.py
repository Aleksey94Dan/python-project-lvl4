"""Logic for home page of tasks"""

from django.urls import reverse_lazy
from django.views.generic.list import ListView
from tasks.forms import TaskListSortForm
from django.views.generic.edit import FormMixin

from tasks.models import Tasks
from user.mixins import CustomRequiredMixin


class TasksListView(CustomRequiredMixin, FormMixin, ListView):
    """Tasks list view."""

    template_name = 'tasks.html'
    form_class = TaskListSortForm
    model = Tasks
    context_object_name = 'tasks'
    login_url = reverse_lazy('login')
