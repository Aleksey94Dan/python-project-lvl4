"""Customized mixins for privileges."""

from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _


class RequiredMixin(AccessMixin):
    """Add a info message on successful logout."""

    redirect_field_name = None
    login_url = reverse_lazy('login')
    error_message = _(
        'You do not have permission to change the user otherwise.'
    )
    permission_denied_message = _(
        'You are not authorized! Please sign in.'
    )

    def dispatch(self, request, *args, **kwargs):
        """Allow the user to edit only their own data."""
        if not request.user.is_authenticated:
            messages.add_message(
                request,
                messages.ERROR,
                self.permission_denied_message,
            )
            return self.handle_no_permission()

        try:
            obj = self.get_object().author
        except AttributeError:
            obj = self.get_object()

        if self.request.user == obj:
            return super().dispatch(request, *args, **kwargs)

        if self.error_message:
            messages.add_message(
                request,
                messages.ERROR,
                self.error_message,
            )
        return HttpResponseRedirect(self.redirect_url)


class NextPageMixin:
    """Blending the transition to the next page."""

    message = None

    def get_next_page(self):
        """Go to next page."""
        next_page = super().get_next_page()
        if self.message:
            messages.add_message(
                self.request,
                messages.SUCCESS,
                self.message,
            )
        return next_page


class DeleteMixin:
    """Allow only unrelated objects to be deleted."""

    success_message_delete = None
    error_message_delete = None

    def delete(self, request, *args, **kwargs):
        """Delete status and display message"""
        try:
            self.get_object().delete()
            messages.add_message(
                request,
                messages.SUCCESS,
                self.success_message_delete,
            )
        except IntegrityError:
            messages.add_message(
                request,
                messages.ERROR,
                self.error_message_delete,
            )
        return HttpResponseRedirect(self.success_url)
