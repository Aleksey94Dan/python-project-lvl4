"""Routes for authorization and registration, users."""

from django.urls import path

from user.views import (
    UserCreateView,
    UserDeleteView,
    UserLoginView,
    UserLogoutView,
    UsersListView,
    UserUpdateView,
)

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('users/create/', UserCreateView.as_view(), name='user-create'),
    path('users/', UsersListView.as_view(), name='users-list'),
    path(
        'users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update',
    ),
    path(
        'users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete',
    ),
]
