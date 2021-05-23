"""task_manager URL Configuration."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    path('', include('statuses.urls')),
    path('', include('labels.urls')),
]
