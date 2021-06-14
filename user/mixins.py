"""Customized mixins for privileges."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _


class CustomRequiredMixin(LoginRequiredMixin):
    """Add a info message on successful logout."""

    login_url = reverse_lazy('home')
    redirect_field_name = None
    info_message = _('Вы разлогинены')
    error_messages = _('Вы не авторизованы! Пожалуйста, выполните вход.')

    def get_next_page(self, **kwargs):  # noqa: WPS615
        """Get redirect page."""
        if self.info_message:
            messages.add_message(
                self.request,
                messages.INFO,
                self.info_message,
            )
        return super().get_next_page(**kwargs)

    def handle_no_permission(self):  # noqa: D102
        if self.error_messages:
            messages.add_message(
                self.request,
                messages.ERROR,
                self.error_messages,
            )
        return super().handle_no_permission()


class UserEditMixin(CustomRequiredMixin, SuccessMessageMixin):
    """
    Overriding get, post, queryset methods

    for user access only to their posts.
    """

    message_error = _('У вас нет прав для изменения другого пользователя.')
    redirect_url = None

    def get_queryset(self):
        """Access to own records only."""
        query_set = super().get_queryset()
        user = self.request.user.pk
        return query_set.filter(id=user)

    def get(self, request, *args, **kwargs):
        """Redirect user if he is not accessing his record."""
        pk = kwargs['pk']
        user = self.request.user.pk
        if pk != user:
            if self.message_error:
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    self.message_error,
                )
            return HttpResponseRedirect(self.redirect_url)
        return super().get(request, *args, **kwargs)


class CustomDeleteMixin:
    """Allow only unrelated objects to be deleted."""

    success_message = None
    error_message = None

    def delete(self, request, *args, **kwargs):
        """Delete status and display message"""
        object_ = self.get_object()  # noqa: WPS120
        related_object_ = object_.task_set.exists()  # noqa: WPS120
        if related_object_:
            messages.add_message(
                request,
                messages.ERROR,
                self.error_message,
            )
            return HttpResponseRedirect(self.success_url)
        messages.add_message(
            request,
            messages.SUCCESS,
            self.success_message,
        )
        return super().delete(request, *args, **kwargs)
