from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from Szamapp.models import MealBaseOptions


class MainForm(forms.Form):
    button = forms.CharField()


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


class Step1Form(forms.Form):
    btn = forms.CharField()


class Step2Form(forms.Form):
    btn = forms.CharField()


class Step3Form(forms.Form):
    meal_type = forms.ModelMultipleChoiceField(
        queryset=MealBaseOptions.objects.all().order_by('id'),
        label="Type",
        widget=forms.CheckboxSelectMultiple
    )


class Step4Form(forms.Form):
    ingredient1 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', "placeholder": "Pierwszy składnik"}),
        required=True
    )
    ingredient2 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', "placeholder": "Drugi składnik"}),
        required=True
    )
    ingredient3 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', "placeholder": "Trzeci składnik"}),
        required=False
    )
    ingredient4 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', "placeholder": "Czwarty składnik"}),
        required=False
    )
    ingredient5 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', "placeholder": "Piąty składnik"}),
        required=False
    )
