"""Login and registration forms."""

from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    password_validation,
)
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class RegistrationForm(UserCreationForm):
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


class LoginForm(AuthenticationForm):
    """Setting up the application login form."""


class UserUpdateForm(forms.ModelForm):
    """Udate user form."""

    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
        )
