from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
import django.contrib.sessions
from Szamapp.forms import *
from Szamapp.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai


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


class UserAccountView(View):
    def get(self, request):
        username = request.user.username
        user = User.objects.get(username=username)

    def post(self, request):
        username = request.user.username
        user = User.objects.get(username=username)
        if "delete" in request.POST:
            user.delete()


class AppStep1View(View):
    def get(self, request):
        form = Step1Form()
        ctx = {
            'form': form
        }
        return render(request, 'pages/step1.html', ctx)

    def post(self, request):
        form = Step1Form(request.POST)
        if form.is_valid():
            val = form.cleaned_data.get("btn")
            request.session['time'] = val
        else:
            form = Step1Form()
            ctx = {
                'form': form
            }
            return render(request, 'pages/step1.html', ctx)
        return redirect('step2')


class AppStep2View(View):
    def get(self, request):
        form = Step2Form()
        ctx = {
            'form': form
        }
        return render(request, 'pages/step2.html', ctx)

    def post(self, request):
        form = Step2Form(request.POST)
        if form.is_valid():
            val = form.cleaned_data.get("btn")
            request.session['base'] = val
            ads = request.session['base']
        else:
            form = Step2Form()
            ctx = {
                'form': form
            }
            return render(request, 'pages/step2.html', ctx)
        return redirect('step3')


class AppStep3View(View):
    def get(self, request):
        form = Step3Form()
        ctx = {
            'form': form
        }
        return render(request, 'pages/step3.html', ctx)

    def post(self, request):
        form = Step3Form(request.POST)
        if form.is_valid():
            meal_type = form.cleaned_data.get("meal_type")
            types = []
            for type in meal_type:
                 types.append(type.name)
            request.session['types'] = types
        else:
            form = Step3Form()
            ctx = {
                'form': form
            }
            return render(request, 'pages/step3.html', ctx)
        return redirect("step4")


class AppStep4View(View):
    def get(self, request):
        form = Step4Form()
        ctx = {
            'form': form
        }
        return render(request, 'pages/step4.html', ctx)

    def post(self, request):
        form = Step4Form(request.POST)
        if form.is_valid():
            ingredient_1 = form.cleaned_data.get("ingredient_1")
            ingredient_2 = form.cleaned_data.get("ingredient_2")
            ingredient_3 = form.cleaned_data.get("ingredient_3")
            ingredient_4 = form.cleaned_data.get("ingredient_4")
            ingredient_5 = form.cleaned_data.get("ingredient_5")
            ingredients = [ingredient_1, ingredient_2]
            if ingredient_3 is not None:
                ingredients.append(ingredient_3)
            else:
                pass
            if ingredient_4 is not None:
                ingredients.append(ingredient_4)
            else:
                pass
            if ingredient_5 is not None:
                ingredients.append(ingredient_5)
            else:
                pass
            request.session['ingredients'] = ingredients
        else:
            form = Step4Form()
            ctx = {
                'form': form
            }
            return render(request, 'pages/step4.html', ctx)
        return redirect("chat")


def chat(request):
    chats = Chat.objects.all()
    return render(request, 'pages/chat.html', {
        'chats': chats,
    })


@csrf_exempt
def Ajax(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check if request is Ajax
        text = request.POST.get('text')
        print(text)
        openai.api_key = "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"
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"{text}"}
            ]
        )
        response = res.choices[0].message["content"]
        print(response)
        chat = Chat.objects.create(
            text=text,
            gpt=response
        )
        return JsonResponse({'data': response, })
    return JsonResponse({})
