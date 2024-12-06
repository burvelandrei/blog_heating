from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "birth_date",
            "email",
            "password1",
            "password2",
        )
        labels = {"username": "Username пользователя", "birth_date": "Дата рождения"}
        widgets = {"birth_date": forms.DateInput(attrs={"type": "date"})}


class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "password")
        labels = {"username": "Username пользователя"}