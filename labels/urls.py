"""Routes for labels."""

from django.urls import path

from labels.views.edit import (
    LabelsCreateView,
    LabelsDeleteView,
    LabelsUpdateView,
)
from labels.views.home import LabelsListView

urlpatterns = [
    path('labels/', LabelsListView.as_view(), name='labels'),
    path(
        'labels/create/',
        LabelsCreateView.as_view(),
        name='labels-create',
    ),
    path(
        'labels/<int:pk>/update/',
        LabelsUpdateView.as_view(),
        name='labels-update',
    ),
    path(
        'labels/<int:pk>/delete/',
        LabelsDeleteView.as_view(),
        name='labels-delete',
    ),
]
