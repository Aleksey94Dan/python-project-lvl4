"""Stores text for flash messages."""


from django.utils.translation import ugettext as _

LABEL_MESSAGES = {
    'succes_create': _('Label created successfully'),
    'succes_update': _('Label changed successfully'),
    'succes_delete': _('Label deleted successfully'),
    'error_delete': _('Cannot remove a label because it is in use'),
}.get

STATUS_MESSAGES = {
    'succes_create': _('Status successfully created'),
    'succes_update': _('Status successfully updated'),
    'succes_delete': _('Status successfully deleted'),
    'error_delete': _('Unable to delete status because it is in use'),
}.get

TASKS_MESSAGES = {
    'succes_create': _('Task successfully created'),
    'succes_update': _('Task successfully updated'),
    'succes_delete': _('Task successfully deleted'),
    'error_delete': _('A task can only be deleted by its author'),
}.get
