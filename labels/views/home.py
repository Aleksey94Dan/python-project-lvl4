"""Logic for home page of labels."""

from django.urls import reverse_lazy
from django.views.generic.list import ListView

from labels.models import Labels
from user.mixins import CustomRequiredMixin


class LabelsListView(CustomRequiredMixin, ListView):
    """Labels list view."""

    template_name = 'labels.html'
    model = Labels
    context_object_name = 'labels'
    login_url = reverse_lazy('login')
