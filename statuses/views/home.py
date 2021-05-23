"""Logic for home page of statuses, tasks, labels."""


from django.urls import reverse_lazy
from django.views.generic.list import ListView

from statuses.models import Statuses
from user.mixins import CustomRequiredMixin


class StatusesListView(CustomRequiredMixin, ListView):
    """Statuses list view."""

    template_name = 'statuses.html'
    model = Statuses
    context_object_name = 'statuses'
    login_url = reverse_lazy('login')
