"""Customized mixins for privileges."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect


class CustomRequiredMixin(LoginRequiredMixin):
    """Add a info message on successful logout."""

    login_url = '/'
    redirect_field_name = None
    info_message = 'Вы разлогинены'
    error_message = 'Вы не авторизованы! Пожалуйста, выполните вход.'

    def get_next_page(self, **kwargs):  # noqa: WPS615
        """Get redirect page."""
        info_message = self.info_message
        if info_message:
            messages.add_message(self.request, messages.INFO, info_message)
        return super().get_next_page(**kwargs)

    def handle_no_permission(self):  # noqa: D102
        error_message = self.error_message
        if error_message:
            messages.add_message(
                self.request,
                messages.ERROR,
                error_message,
            )
        return super().handle_no_permission()


class UserEditMixin(CustomRequiredMixin, SuccessMessageMixin):
    """
    Overriding get, post, queryset methods

    for user access only to their posts.
    """

    message_error = None
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
        message_error = self.message_error
        if pk != user:
            if message_error:
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    message_error,
                )
            return HttpResponseRedirect(self.redirect_url)
        return super().get(request, *args, **kwargs)
