from django import forms


class LoginForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder':'Имя пользователя',
            'type': 'name',
            'class': 'form-control',
            'id': 'InputName',
            'aria-describedby':'nameHelp',
        },
    ))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Пароль',
            'type': "password",
            'class': 'form-control',
            'id': 'InputPassword',
        },
    ))



class RegisterForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Имя',
                'type': 'FirstName',
                'class': 'form-control',
                'id': 'InputFirstName',
                'aria-describedby': 'firstNameHelp'
            },
        ),
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Фамилия',
                'type': 'LastName',
                'class': 'form-control',
                'id': 'InputLastName',
            },
        ),
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder':'Имя пользователя',
            'type': 'name',
            'class': 'form-control',
            'id': 'InputName',
            'aria-describedby':'nameHelp',
            'title': 'Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.',
        },
    ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Пароль',
            'type': "password1",
            'class': 'form-control',
            'id': 'InputPassword1',
            'title': 'Ваш пароль должен содержать как минимум 3 символа.',
        },
    ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Пароль',
            'type': "password2",
            'class': 'form-control',
            'id': 'InputPassword2',
            'title': 'Для подтверждения введите, пожалуйста, пароль ещё раз.'
        },
    ))

