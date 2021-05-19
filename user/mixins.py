"""Customized mixins for privileges."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomLogoutMixin(LoginRequiredMixin):
    """Add a info message on successful logout."""

    info_message = 'Вы разлогинены'

    def get_next_page(self, **kwargs):  # noqa: WPS615
        """Get redirect page."""
        info_message = self.info_message
        if info_message:
            messages.add_message(self.request, messages.INFO, info_message)
        return super().get_next_page(**kwargs)


class CustomEditUserMixin(LoginRequiredMixin):
    """Add info error while editing."""

    error_message = 'Вы не авторизованы! Пожалуйста, выполните вход.'

    login_url = '/login'
    redirect_field_name = None

    def handle_no_permission(self):  # noqa: D102
        error_message = self.error_message
        if error_message:
            messages.add_message(
                self.request,
                messages.ERROR,
                error_message,
            )
        return super().handle_no_permission()
