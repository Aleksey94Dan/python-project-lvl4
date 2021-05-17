"""Routes for authorization and registration."""

from django.urls import path

from user.views import (
    CustomLoginView,
    CustomLogoutView,
    HomeView,
    UserCreateView,
    UserDeleteView,
    UsersListView,
    UserUpdateView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('users/create/', UserCreateView.as_view(), name='user-create'),
    path('users/', UsersListView.as_view(), name='users-list'),
    path(
        'users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update',
    ),
    path(
        'users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete',
    ),
]
