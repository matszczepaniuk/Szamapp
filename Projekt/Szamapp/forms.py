from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from Szamapp.models import User


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Username'}),
    )
    email = forms.CharField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Email'}),
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        label="Password Confirmation",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-control-lg', 'placeholder': 'Password Confirmation'}),
    )


class UserLoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={"class": "form-control form-control-lg", "placeholder": "Login"}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-lg", "placeholder": "Password"}),
    )
