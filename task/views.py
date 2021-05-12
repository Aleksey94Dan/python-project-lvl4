
"""Views for task_manager."""

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render

from task.forms import LoginForm, RegisterForm
from task.models import Label, Status, Task


def index(request):
    """Home page view."""
    return render(request, 'task/index.html', {'title': 'home'})


def users(request):
    """User withdrawal."""
    users = User.objects.all()
    return render(
        request, 'task/users.html', {'title': 'users', 'users': users},
    )


def create_user(request):
    """Create users."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            login(request, user)
            messages.success(request, 'Пользователь успешно зарегистрирован')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(
        request, 'task/create_user.html', {
            'title': 'create_users', 'form': form,
            },
        )


def log_in(request):
    """Login to the application."""
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                username=cd['username'],
                password = cd['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы залогинены')
                return redirect('home')
        return render(
            request, 'task/login.html', {
                'title': 'login', 'form': form,
            },
        )
    else:
        form = LoginForm()
    return render(
        request, 'task/login.html', {
            'title': 'login', 'form': form,
        },
    )


def delete_user_view(request, pk):
    """Delete Users."""
    username = User.objects.filter(pk=pk)[0].username
    return HttpResponse('Вы уверены, что хотите удалить пользователя {}'.format(username))


def update_user_view(request, pk):
    """Update Users."""
    username = User.objects.filter(pk=pk)[0].username
    return HttpResponse('Изменение пользователя {}'.format(username))


def log_out(request):
    """Log out from the application."""
    logout(request)
    messages.info(request, 'Вы разлогинены')
    return redirect('login')


def statuses_view(request):
    """Representation of statuses."""
    statuses = Status.objects.all()
    return render(
        request, 'task/statuses.html', {
            'title': 'statuses', 'statuses': statuses,
        },
    )


def labels_view(request):
    """Representation of labels."""
    labels = Label.objects.all()
    return render(
        request, 'task/labels.html', {
            'title': 'labels', 'labels': labels,
        },
    )


def tasks_view(request):
    """Representation of tasks."""
    tasks = Task.objects.all()
    return render(
        request, 'task/tasks.html', {
            'title': 'tasks', 'tasks': tasks,
        },
    )


def tasks_create_view(request):
    """Create tasks."""
    return HttpResponse('Создать задачу')


def statuses_create_view(request):
    """Create status."""
    return HttpResponse('Создать статус')


def labels_create_view(request):
    """Create label."""
    return HttpResponse('Cоздать метку')


def delete_label_view(request):
    """Delete label."""
    return HttpResponse('Удалить метку')


def update_label_view(request):
    """Update label."""
    return HttpResponse('Обновить метку')


def delete_status_view(request):
    """Delete status."""
    return HttpResponse('Удалить статус')


def update_status_view(request):
    """Update status."""
    return HttpResponse('Обновить статус')


def update_task_view(request):
    """Update task."""
    return HttpResponse('Обновить задачу')


def delete_task_view(request):
    """Delete task."""
    return HttpResponse('Удалить задачу')
