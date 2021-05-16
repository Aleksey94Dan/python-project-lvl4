"""Logic for login and registration."""

from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from user.forms import LoginForm, RegistrationForm, UserUpdateForm


class UserCreateView(CreateView):
    """User registration view."""

    template_name = 'registration/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')


class CustomLoginView(LoginView):
    """User login view."""

    template_name = 'registration/login.html'
    form_class = LoginForm

    def get_success_url(self):
        """Redirect after successful check."""
        return reverse_lazy('home')


class CustomLogoutView(LogoutView):
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


class UserUpdateView(UpdateView):
    """Change user data."""

    template_name = 'updating.html'
    form_class = UserUpdateForm
    model = User
    success_url = reverse_lazy('home')


class UserDeleteView(DeleteView):
    """Delete user data."""

    model = User
    template_name = 'deleting.html'
    success_url = reverse_lazy('home')
