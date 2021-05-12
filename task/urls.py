"""Configuration routing."""

from django.urls import path

from task.views import (
    create_user,
    delete_label_view,
    delete_status_view,
    delete_task_view,
    delete_user_view,
    index,
    labels_create_view,
    labels_view,
    log_in,
    log_out,
    statuses_create_view,
    statuses_view,
    tasks_create_view,
    tasks_view,
    update_label_view,
    update_status_view,
    update_task_view,
    update_user_view,
    users,
)

urlpatterns = [
    path('', index, name='home'),

    path('users/', users, name='users'),
    path('users/create/', create_user, name='create-user'),
    path('users/<int:pk>/update/', update_user_view, name='update-user'),
    path('users/<int:pk>/delete/', delete_user_view, name='delete-user'),

    path('login/', log_in, name='login'),
    path('logout/', log_out, name='logout'),

    path('statuses/', statuses_view, name='statuses'),
    path('statuses/create/', statuses_create_view, name='statuses-create'),
    path('statuses/<int:pk>/update/', update_status_view, name='update-status'),
    path('statuses/<int:pk>/delete/', delete_status_view, name='delete-status'),


    path('labels/', labels_view, name='labels'),
    path('labels/create', labels_create_view, name='labels-create'),
    path('labels/<int:pk>/update/', update_label_view, name='update-label'),
    path('labels/<int:pk>/delete/', delete_label_view, name='delete-label'),


    path('tasks/', tasks_view, name='tasks'),
    path('tasks/create', tasks_create_view, name='tasks-create'),
    path('task/<int:pk>/update/', update_task_view, name='update-task'),
    path('task/<int:pk>/delete/', delete_task_view, name='delete-task'),
]
