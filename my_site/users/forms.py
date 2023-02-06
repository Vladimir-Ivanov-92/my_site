from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from users.models import User
from users.tasks import send_email_verification


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label="Имя пользователя", widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Введите имя пользователя"
    }))
    email = forms.CharField(label="Адрес электронной почты", widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Введите адрес эл. почты"
    }))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Введите пароль"
    }))
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Повторите пароль"
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        send_email_verification.delay(user.id)
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя", widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Введите имя пользователя"
    }))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Введите пароль",
    }))

    class Meta:
        model = User
        fields = ['username', 'password']
