"""Routes for statuses."""

from django.urls import path

from statuses.views.edit import (
    StatusesCreateView,
    StatusesDeleteView,
    StatusesUpdateView,
)
from statuses.views.home import StatusesListView

urlpatterns = [
    path('statuses/', StatusesListView.as_view(), name='statuses'),
    path(
        'statuses/create/',
        StatusesCreateView.as_view(),
        name='statuses-create',
    ),
    path(
        'statuses/<int:pk>/update/',
        StatusesUpdateView.as_view(),
        name='statuses-update',
    ),
    path(
        'statuses/<int:pk>/delete/',
        StatusesDeleteView.as_view(),
        name='statuses-delete',
    ),
]
