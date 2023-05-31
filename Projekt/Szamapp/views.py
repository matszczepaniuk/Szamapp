from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from Szamapp.forms import *
from Szamapp.models import *

# Create your views here.


def index(request):
    # Page from the theme
    return render(request, 'pages/index.html')


class UserLoginView(View):
    def get(self, request):
        form = UserLoginForm
        ctx = {
            'form': form
        }
        return render(request, 'pages/login.html', ctx)

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            message = "Zalogowano"
        else:
            return render(request, 'pages/login.html')
        return render(request, 'pages/registration.html', context={'message': message})



class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        ctx = {
            'form': form
        }
        return render(request, 'pages/registration.html', ctx)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password1 = request.POST["password1"]
            password2 = request.POST["password2"]
            email = request.POST["email"]
            if password1 == password2:
                new_user = User.objects.create_user(username=username, email=email, password=password1)
                return redirect('login')
            else:
                return redirect('login')
