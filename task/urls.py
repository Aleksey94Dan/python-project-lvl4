"""Configuration routing."""

from django.urls import path

from task.views import create_user, index, login, users

urlpatterns = [
    path('', index, name='home'),
    path('users/', users, name='users'),
    path('users/create/', create_user, name='create_user'),
    path('login/', login, name='login'),
]
