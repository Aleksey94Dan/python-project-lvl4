"""task_manager URL Configuration."""

from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="home.html"), name='home'),
    path('', include('user.urls')),
    path('', include('statuses.urls')),
    path('', include('labels.urls')),
    path('', include('tasks.urls')),
    path('i18n', include('django.conf.urls.i18n')),
]
