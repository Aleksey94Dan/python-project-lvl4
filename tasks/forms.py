"""Description of forms for tasks."""


from django.forms import ModelForm

from tasks.models import Task


class TaskForm(ModelForm):
    """Tasks."""

    class Meta:
        model = Task
        exclude = ['author']
