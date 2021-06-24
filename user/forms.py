"""Login and registration forms."""

from django.contrib.auth.forms import UserCreationForm

from user.models import User


class AuthForm(UserCreationForm):
    """Setting up the registration form in the application."""

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        )
