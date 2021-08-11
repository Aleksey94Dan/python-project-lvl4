from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _


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
