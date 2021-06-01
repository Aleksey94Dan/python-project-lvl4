"""Login and logout views."""

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView

from user.forms import LoginForm, RegistrationForm
from user.mixins import CustomRequiredMixin


class CustomLoginView(SuccessMessageMixin, LoginView):
    """User login view."""

    template_name = 'registration/login.html'
    form_class = LoginForm
    success_message = _('You are logged in')

    def get_success_url(self):
        """Redirect after successful check."""
        return reverse_lazy('home')


class CustomLogoutView(CustomRequiredMixin, LogoutView):
    """User logout view."""

    next_page = reverse_lazy('home')


class UserCreateView(SuccessMessageMixin, CreateView):
    """User registration view."""

    template_name = 'registration/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    success_message = _('User registered successfully')
