"""Views for task_manager."""

from django.shortcuts import render
from task.form import LoginForm, RegisterForm


def index(request):
    return render(request, 'task/index.html', {'title': 'home'})


def users(request):
    return render(request, 'task/users.html', {'title': 'users'})


def create_user(request):
    form = RegisterForm()
    return render(request, 'task/create_user.html', {'title': 'create_users', 'form': form})


def login(request):
    form = LoginForm()
    return render(request, 'task/login.html', {'title': 'login', 'form': form})