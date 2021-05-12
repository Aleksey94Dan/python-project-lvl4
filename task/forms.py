from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    """Setting up the application login form."""

    username = forms.CharField(
        label='Имя пользователя',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Имя пользователя',
                'autocomplete': 'username',
                'type': 'text',
                'class': 'form-control',
                'id': 'id_username',
            },
        ),
    )
    password = forms.CharField(
            label='Пароль',
            label_suffix='',
            widget=forms.TextInput(
                attrs={
                    'name': 'password',
                    'autocomplete': 'current-password',
                    'placeholder': 'Пароль',
                    'type': 'password',
                    'class': 'form-control',
                    'id': 'id_password',
                },
            ),
        )


class RegisterForm(UserCreationForm):
    """Setting up the registration form in the application."""

    first_name = forms.CharField(
        max_length=30,
        label='Имя',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Имя',
                'type': 'text',
                'class': 'form-control',
                'id': 'id_first_name',
            },
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        label='Фамилия',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Фамилия',
                'type': 'text',
                'class': 'form-control',
                'id': 'id_last_name',
            },
        ),
    )
    username = forms.CharField(
        max_length=30,
        help_text='Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.',
        label='Имя пользователя',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Имя пользователя',
                'type': 'text',
                'class': 'form-control',
                'id': 'id_username',
                'title': 'Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.',
            },
        ),
    )
    password1 = forms.CharField(
        label='Пароль',
        help_text='Ваш пароль должен содержать как минимум 3 символа.',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'name': 'password1',
                'autocomplete': 'new-password',
                'placeholder': 'Пароль',
                'type': 'password',
                'class': 'form-control',
                'id': 'id_password1',
                'title': 'Ваш пароль должен содержать как минимум 3 символа.',
            },
        ),
    )

    password2 = forms.CharField(
        label='Подтверждение пароля',
        label_suffix='',
        help_text='Для подтверждения введите, пожалуйста, пароль ещё раз.',
        widget=forms.TextInput(
            attrs={
                'name': 'password2',
                'autocomplete': 'new-password',
                'placeholder': 'Подтверждение пароля',
                'type': 'password',
                'class': 'form-control',
                'id': 'id_password2',
                'title': 'Для подтверждения введите, пожалуйста, пароль ещё раз.',
            },
        ),
    )

    class Meta(UserCreationForm):
        """We set the model for the form.

        Determine the order of the output of the fields.
        """

        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        )
