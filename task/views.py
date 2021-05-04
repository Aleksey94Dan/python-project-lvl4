"""Views for task_manager."""

from django.shortcuts import render


def index(request):
    return render(request, 'task/index.html', {'title': 'home'})


def users(request):
    return render(request, 'task/users.html', {'title': 'users'})


def create_user(request):
    return render(request, 'task/create_user.html', {'title': 'create_users'})


def login(request):
    return render(request, 'task/login.html', {'title': 'login'})