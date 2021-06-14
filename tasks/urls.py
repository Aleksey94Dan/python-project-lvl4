"""Routes for tasks."""

from django.urls import path

from tasks.views import (
    TasksCreateView,
    TasksDeleteView,
    TasksListView,
    TasksTicketView,
    TasksUpdateView,
)

urlpatterns = [
    path('tasks/', TasksListView.as_view(), name='tasks'),
    path('tasks/<int:pk>/', TasksTicketView.as_view(), name='task-ticket'),
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
