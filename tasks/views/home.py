"""Logic for home page of tasks"""

from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView

from labels.models import Labels
from statuses.models import Statuses
from tasks.forms import TaskListSortForm
from tasks.models import Tasks
from user.mixins import CustomRequiredMixin


class TasksListView(CustomRequiredMixin, FormMixin, ListView):
    """Tasks list view."""

    template_name = 'tasks.html'
    form_class = TaskListSortForm
    model = Tasks
    context_object_name = 'tasks'
    login_url = reverse_lazy('login')


    def get_form_kwargs(self, **kwargs):
        kwargs.update({
           'statuses': Statuses.objects.all(),
           'labels': Labels.objects.all(),
           'executor': User.objects.filter(is_staff=False),
        })
        return kwargs


    # def get_queryset(self):
    #     filter_dict = self.request.GET.dict()
    #     new_context = Tasks.objects.filter(**filter_dict)
    #     return new_context
