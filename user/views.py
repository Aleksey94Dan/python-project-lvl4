"""Logic for login and registration."""

from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from user.forms import LoginForm, RegistrationForm, UserUpdateForm
from user.mixins import CustomRequiredMixin, UserEditMixin


class UserCreateView(SuccessMessageMixin, CreateView):
    """User registration view."""

    template_name = 'registration/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    success_message = 'Пользователь успешно зарегистрирован'


class CustomLoginView(SuccessMessageMixin, LoginView):
    """User login view."""

    template_name = 'registration/login.html'
    form_class = LoginForm
    success_message = 'Вы залогинены'

    def get_success_url(self):
        """Redirect after successful check."""
        return reverse_lazy('home')


class CustomLogoutView(CustomRequiredMixin, LogoutView):
    """User logout view."""

    next_page = 'home'


class UsersListView(ListView):
    """User list view."""

    template_name = 'users.html'
    model = User
    context_object_name = 'users'


class HomeView(TemplateView):
    """Home page view."""

    template_name = 'home.html'


class UserUpdateView(UserEditMixin, UpdateView):
    """Change user data."""

    template_name = 'updating.html'
    form_class = UserUpdateForm
    model = User
    success_url = reverse_lazy('home')
    success_message = 'Пользователь успешно изменен'
    message_error_for_get = 'У вас нет прав для изменения другого пользователя.'
    redirect_url = reverse_lazy('users-list')


class UserDeleteView(UserEditMixin, DeleteView):
    """Delete user data."""

    model = User
    template_name = 'deleting.html'
    success_url = reverse_lazy('home')
    message_error_for_post = 'Невозможно удалить пользователя, потому что он используется'
    message_error_for_get = 'У вас нет прав для изменения другого пользователя.'
    redirect_url = reverse_lazy('users-list')
