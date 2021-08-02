"""Customized mixins for privileges."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _


class AuthRequiredMixin(LoginRequiredMixin):
    """Add a info message on successful logout."""

    redirect_url = reverse_lazy('login')
    permission_denied_message = _(
        'You are not authorized! Please sign in.'
    )

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return HttpResponseRedirect(self.redirect_url)


class UserTestAccountMixin(UserPassesTestMixin):
    """Check user."""

    def test_func(self):
        return self.get_object() == self.request.user

    def dispatch(self, request, *args, **kwargs):
        self.permission_denied_message = _(
            'You do not have permission to change the user otherwise.'
        )
        self.redirect_url = reverse_lazy('users-list')
        return super().dispatch(request, *args, **kwargs)


class TaskTestAccountMixin(UserPassesTestMixin):
    """Check test."""

    def test_func(self):
        return self.get_object().author == self.request.user

    def dispatch(self, request, *args, **kwargs):
        self.permission_denied_message = _(
            'A task can only be deleted by its author'
        )
        self.redirect_url = reverse_lazy('tasks')
        return super().dispatch(request, *args, **kwargs)


class DeleteMixin:
    """Allow only unrelated objects to be deleted."""

    success_message_delete = None
    error_message_delete = None

    def delete(self, request, *args, **kwargs):
        """Delete status and display message"""
        try:
            ctx = super().delete(request, *args, **kwargs)
            messages.add_message(request, messages.SUCCESS, self.success_message_delete)
            return ctx
        except ProtectedError:
            messages.add_message(request, messages.ERROR, self.error_message_delete)
        return HttpResponseRedirect(self.success_url)
