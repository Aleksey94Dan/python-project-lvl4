"""Configuration routing."""

from django.urls import path
from task.views import GreetingView

urlpatterns = [
    path('greeting/', GreetingView.as_view(), name='greeting'),
]