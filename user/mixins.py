"""Customized mixins for privileges."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect


class CustomRequiredMixin(LoginRequiredMixin):
    """Add a info message on successful logout."""

    login_url = '/login'
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


class UserEditMixin(CustomRequiredMixin):
    """
    Overriding get, post, queryset methods

    for user access only to their posts.
    """

    message_error_for_get = ''
    message_error_for_post = ''
    redirect_url = ''

    def get_queryset(self):
        """Access to own records only."""
        query_set = super().get_queryset()
        user = self.request.user.pk
        return query_set.filter(id=user)

    def get(self, request, *args, **kwargs):
        """Redirect user if he is not accessing his record."""
        pk = kwargs['pk']
        user = self.request.user.pk
        message_error_for_get = self.message_error_for_get
        if pk != user:
            if message_error_for_get:
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    message_error_for_get,
                )
            return HttpResponseRedirect(self.redirect_url)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Prevent user from deleting himself."""
        message_error_for_post = self.message_error_for_post
        if message_error_for_post:
            messages.add_message(
                self.request,
                messages.ERROR,
                message_error_for_post,
            )
        return HttpResponseRedirect(self.redirect_url)
