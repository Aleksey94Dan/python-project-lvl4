from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _


class LabelDeleteMixin:
    """Delete mixin for labels."""

    def delete(self, request, *args, **kwargs):  # noqa: D102
        if self.get_object().task_set.exists():
            messages.add_message(
                request,
                messages.ERROR,
                _('Cannot remove a label because it is in use'),
            )
            return HttpResponseRedirect(self.success_url)
        messages.add_message(
            request,
            messages.SUCCESS,
            _('Label deleted successfully'),
        )
        return super().delete(request, *args, **kwargs)
