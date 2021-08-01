"""Logic for users."""

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from task_manager.mixins import AuthRequiredMixin, DeleteMixin
from user.forms import AuthForm
from user.models import User


class UserLoginView(SuccessMessageMixin, LoginView):
    """User login view."""

    template_name = 'registration/login.html'
    form_class = AuthenticationForm
    success_message = _('You are logged in')


class UserLogoutView(LogoutView):
    """User logout view."""

    next_page = reverse_lazy('home')
    message = _('You are logged out')

    def dispatch(self, request, *args, **kwargs):
        """Add message to dispatch."""
        messages.info(request, self.message)
        return super().dispatch(request, *args, **kwargs)


class UsersListView(ListView):
    """User list view."""

    template_name = 'users.html'
    model = User
    context_object_name = 'users'


class UserUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    """Change user data."""

    template_name = 'update.html'
    form_class = AuthForm
    model = User

    login_url = reverse_lazy('login')
    redirect_url = reverse_lazy('users-list')
    success_url = redirect_url

    success_message = _('User changed successfully')


class UserDeleteView(AuthRequiredMixin, DeleteMixin, DeleteView):
    """Delete user data."""

    template_name = 'delete.html'
    model = User

    login_url = reverse_lazy('login')
    redirect_url = reverse_lazy('users-list')
    success_url = reverse_lazy('users-list')

    success_message_delete = _('User deleted successfully')
    error_message_delete = _('Unable to delete user because he is in use')


class UserCreateView(SuccessMessageMixin, CreateView):
    """User registration view."""

    template_name = 'registration/registration.html'
    form_class = AuthForm
    success_url = reverse_lazy('login')
    success_message = _('User registered successfully')
