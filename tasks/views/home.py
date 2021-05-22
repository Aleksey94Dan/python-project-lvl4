"""Logic for home page of statuses, tasks, labels."""


from django.views.generic.list import ListView

from tasks.models.models import Statuses


class StatusesListView(ListView):
    """Statuses list view."""

    template_name = 'statuses.html'
    model = Statuses
    context_object_name = 'statuses'
