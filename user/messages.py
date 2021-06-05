"""Stores text for flash messages."""


from django.utils.translation import gettext as _

USER_MESSAGES = {
    'succes_create': _('Пользователь успешно зарегистрирован'),
    'succes_update': _('Пользователь успешно изменён'),
    'succes_delete': _('Пользователь успешно удалён'),
    'succes_login': _('Вы залогинены'),
    'error_delete': _(
        'Невозможно удалить пользователя, потому что он используется',
    ),
    'error_update': _('У вас нет прав для изменения другого пользователя.'),
}.get

LABEL_MESSAGES = {
    'succes_create': _('Метка успешно создана'),
    'succes_update': _('Метка успешно изменена'),
    'succes_delete': _('Метка успешно удалена'),
    'error_delete': _('Невозможно удалить метку, потому что она используется'),
}.get

STATUS_MESSAGES = {
    'succes_create': _('Статус успешно создан'),
    'succes_update': _('Статус успешно изменён'),
    'succes_delete': _('Статус успешно удалён'),
    'error_delete': _('Невозможно удалить статус, потому что он используется'),
}.get

TASKS_MESSAGES = {
    'succes_create': _('Задача успешно создана'),
    'succes_update': _('Задача успешно изменена'),
    'succes_delete': _('Задача успешно удалена'),
    'error_delete': _('Задачу может удалить только её автор'),
}.get
