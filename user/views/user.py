"""Logic for users."""

from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.list import ListView

from user.forms import UserUpdateForm
from user.mixins import UserEditMixin


class UsersListView(ListView):
    """User list view."""

    template_name = 'users.html'
    model = User
    context_object_name = 'users'


class UserUpdateView(UserEditMixin, UpdateView):
    """Change user data."""

    model = User
    template_name = 'updating.html'
    form_class = UserUpdateForm

    login_url = reverse_lazy('login')
    redirect_url = reverse_lazy('users-list')
    success_url = redirect_url

    success_message = _('User changed successfully')
    message_error = _(
        'You do not have permission to change another user.',
    )

    @method_decorator(never_cache)
    def post(self, request, *args, **kwargs):
        """Log out after change."""
        query = super().post(request, *args, **kwargs)
        auth_logout(request)
        return query


class UserDeleteView(UserEditMixin, DeleteView):
    """Delete user data."""

    login_url = reverse_lazy('login')
    model = User
    template_name = 'deleting.html'
    success_url = reverse_lazy('home')
    message_error = _(
        'You do not have permission to change another user.',
    )
    message_error_for_post = _(
        'Unable to delete user because he is in use',
    )
    redirect_url = reverse_lazy('users-list')
    extra_context = {'header': _('Deleting a user')}

    def post(self, request, *args, **kwargs):
        """Prevent user from deleting himself."""
        message_error = self.message_error_for_post
        if message_error:
            messages.add_message(
                self.request,
                messages.ERROR,
                message_error,
            )
        return HttpResponseRedirect(self.redirect_url)
