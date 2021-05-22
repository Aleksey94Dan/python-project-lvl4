"""Logic for login and registration."""

from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.contrib import messages
from django.http import HttpResponseRedirect

from user.forms import LoginForm, RegistrationForm, UserUpdateForm
from user.mixins import CustomRequiredMixin, UserEditMixin


class UserCreateView(SuccessMessageMixin, CreateView):
    """User registration view."""

    template_name = 'registration/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')
    success_message = _('Пользователь успешно зарегистрирован')


class CustomLoginView(SuccessMessageMixin, LoginView):
    """User login view."""

    template_name = 'registration/login.html'
    form_class = LoginForm
    success_message = _('Вы залогинены')

    def get_success_url(self):
        """Redirect after successful check."""
        return reverse_lazy('home')


class CustomLogoutView(CustomRequiredMixin, LogoutView):
    """User logout view."""

    next_page = reverse_lazy('home')


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
    login_url=reverse_lazy('login')
    template_name = 'updating.html'
    form_class = UserUpdateForm
    model = User
    success_url = reverse_lazy('home')
    message_error = _(
        'У вас нет прав для изменения другого пользователя.',
    )
    redirect_url = reverse_lazy('users-list')
    success_message = _('Пользователь успешно изменен')






class UserDeleteView(UserEditMixin, DeleteView):
    """Delete user data."""
    login_url=reverse_lazy('login')
    model = User
    template_name = 'deleting.html'
    success_url = reverse_lazy('home')
    message_error = _(
        'У вас нет прав для изменения другого пользователя.',
    )
    redirect_url = reverse_lazy('users-list')

    def post(self, request, *args, **kwargs):
        """Prevent user from deleting himself."""
        message_error_post = _(
            'Невозможно удалить пользователя, потому что он используется',
        )
        if message_error_post:
            messages.add_message(
                self.request,
                messages.ERROR,
                message_error_post,
            )
        return HttpResponseRedirect(self.redirect_url,)