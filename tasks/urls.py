"""Routes for tasks."""

from django.urls import path

from tasks.views.edit import TasksCreateView, TasksDeleteView, TasksUpdateView
from tasks.views.home import TasksListView

urlpatterns = [
    path('tasks', TasksListView.as_view(), name='tasks'),
    path(
        'tasks/create/',
        TasksCreateView.as_view(),
        name='tasks-create',
    ),
    path(
        'tasks/<int:pk>/update/',
        TasksUpdateView.as_view(),
        name='tasks-update',
    ),
    path(
        'tasks/<int:pk>/delete/',
        TasksDeleteView.as_view(),
        name='tasks-delete',
    ),
]