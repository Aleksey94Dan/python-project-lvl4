"""Logic for users."""

from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from user.forms import UserUpdateForm
from user.messages import USER_MESSAGES
from user.mixins import CustomDeleteViewMixin, UserEditMixin
from user.models import CustomUser


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

    success_message = USER_MESSAGES('succes_update')
    message_error = USER_MESSAGES('error_update')

    @method_decorator(never_cache)
    def post(self, request, *args, **kwargs):
        """Log out after change."""
        query = super().post(request, *args, **kwargs)
        auth_logout(request)
        return query


class UserDeleteView(CustomDeleteViewMixin):
    """Delete user data."""

    template_name = 'deleting.html'
    success_message = USER_MESSAGES('succes_delete')
    error_message = USER_MESSAGES('error_delete')
    error_update_message = USER_MESSAGES('error_update')
    model = CustomUser
    extra_context = {'header': _('Удаление пользователя ')}
    success_url = reverse_lazy('users-list')
    login_url = reverse_lazy('login')
    redirect_url = reverse_lazy('users-list')

    def get_queryset(self):
        """Access to own records only."""
        query_set = super().get_queryset()
        user = self.request.user.pk
        return query_set.filter(id=user)

    def get(self, request, *args, **kwargs):
        """Redirect user if he is not accessing his record."""
        pk = kwargs['pk']
        user = self.request.user.pk
        message_error = self.error_update_message
        if pk != user:
            if message_error:
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    message_error,
                )
            return HttpResponseRedirect(self.redirect_url)
        return super().get(request, *args, **kwargs)
