"""Logic for users."""

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from user.forms import AuthForm
from user.mixins import CustomDeleteMixin, CustomRequiredMixin, UserEditMixin
from user.models import CustomUser


class UsersListView(ListView):
    """User list view."""

    template_name = 'users.html'
    model = CustomUser
    context_object_name = 'users'


class UserUpdateView(UserEditMixin, UpdateView):
    """Change user data."""

    template_name = 'updates.html'
    form_class = AuthForm
    model = CustomUser

    login_url = reverse_lazy('login')
    redirect_url = reverse_lazy('users-list')
    success_url = redirect_url

    success_message = _('Пользователь успешно изменен')


class UserDeleteView(UserEditMixin, CustomDeleteMixin, DeleteView):
    """Delete user data."""

    template_name = 'removes.html'
    model = CustomUser

    login_url = reverse_lazy('login')
    redirect_url = reverse_lazy('users-list')
    success_url = reverse_lazy('users-list')

    success_message = _('Пользователь успешно удалён')

    error_message = _(
        'Невозможно удалить пользователя, потому что он используется',
    )


class CustomLoginView(SuccessMessageMixin, LoginView):
    """User login view."""

    template_name = 'registration/login.html'
    form_class = AuthenticationForm
    success_message = _('Вы залогинены')

    def get_success_url(self):
        """Redirect after successful check."""
        return reverse_lazy('home')


class CustomLogoutView(CustomRequiredMixin, LogoutView):
    """User logout view."""

    next_page = reverse_lazy('home')


class UserCreateView(SuccessMessageMixin, CreateView):
    """User registration view."""

    template_name = 'registration/registration.html'
    form_class = AuthForm
    success_url = reverse_lazy('login')
    success_message = _('Пользователь успешно зарегистрирован')
