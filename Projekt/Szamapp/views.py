from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from Szamapp.forms import *
from Szamapp.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import openai
from django.conf import settings


def index(request):
    return render(request, 'pages/index.html')


def main(request):
    if request.user is not None:
        return redirect('step1')
    return render(request, 'pages/main.html')


@csrf_protect
def userlogin(request):
    if request.method == 'GET':
        if request.user is not None:
            return redirect('step1')
        form = UserLoginForm
        ctx = {
            'form': form
        }
        return render(request, 'pages/login.html', ctx)

    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return render(request, 'pages/login.html')
        return redirect('step1')


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
            username = form.cleaned_data.get("username")
            password1 = form.cleaned_data.get("password1")
            password2 = form.cleaned_data.get("password2")
            email = form.cleaned_data.get("email")
            if password1 == password2:
                new_user = User.objects.create_user(username=username, email=email, password=password1)
                return redirect('login')
            else:
                form = RegistrationForm(request.POST)
                ctx = {
                    'form': form
                }
                return render(request, 'pages/registration.html', ctx)
        else:
            form = RegistrationForm(request.POST)
            ctx = {
                'form': form
            }
            return render(request, 'pages/registration.html', ctx)


class UserAccountView(View):
    def get(self, request):
        if request.user.is_authenticated:
            username = request.user.get_username()
            user = User.objects.get(username=username)
            user_id = user.id
            saved_recipes = FavouriteRecipes.objects.filter(user_id_id=user_id)
            return render(request, 'pages/account.html', {'saved_recipes': saved_recipes})
        else:
            return redirect('login')

    def post(self, request):
        username = request.user.username
        user = User.objects.get(username=username)
        if "delete" in request.POST:
            user.delete()
        return render(request, 'pages/account.html')


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
            ingredient_1 = form.cleaned_data.get("ingredient1")
            ingredient_2 = form.cleaned_data.get("ingredient2")
            ingredient_3 = form.cleaned_data.get("ingredient3")
            ingredient_4 = form.cleaned_data.get("ingredient4")
            ingredient_5 = form.cleaned_data.get("ingredient5")
            ingredients = [ingredient_1, ingredient_2]
            i1 = Ingredient.objects.create(name=ingredient_1)
            i1.save()
            i2 = Ingredient.objects.create(name=ingredient_2)
            i2.save()
            if ingredient_3 is not None:
                ingredients.append(ingredient_3)
                i3 = Ingredient.objects.create(name=ingredient_3)
                i3.save()
            if ingredient_4 is not None:
                ingredients.append(ingredient_4)
                i4 = Ingredient.objects.create(name=ingredient_4)
                i4.save()
            if ingredient_5 is not None:
                ingredients.append(ingredient_5)
                i5 = Ingredient.objects.create(name=ingredient_5)
                i5.save()
            else:
                pass
            request.session['ingredients'] = ingredients
        else:
            form = Step4Form()
            ctx = {
                'form': form
            }
            return render(request, 'pages/step4.html', ctx)
        chat = Ajax(request)
        return redirect("step5")


class AppStep5View(View):
    def get(self, request):
        return render(request, 'pages/step5.html')

    def post(self, request):
        offer1 = request.session.get('offer1')
        offer2 = request.session.get('offer2')
        offer3 = request.session.get('offer3')
        return redirect("step4")


def chat(request):
    chats = Chat.objects.all()
    return render(request, 'pages/chat.html', {
        'chats': chats,
    })


@csrf_exempt
def Ajax(request):
    meal_time = request.session.get('time')
    meal_base = request.session.get('base')
    meal_type = request.session.get('types')
    meal_ingredients = request.session.get('ingredients')
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check if request is Ajax
        text = f"Podaj 3 propozycje przepisów na {meal_type} z następujących produktów: {meal_base}, {meal_ingredients}" \
               f", czas przygotowania do {meal_time}, możesz dorzucić jakieś produkty od siebie, na razie nie " \
               f"podawaj także instrukcji przygotowania."
        print(text)
        openai.api_key = settings.OPENAI_API_KEY
        print(openai)
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"{text}"}
            ]
        )
        response = res.choices[0].message["content"]
        print(res)
        offers = []
        response.split('2')
        offers.append(response[0])
        part_response = response[1]
        part_response.split('3')
        offers.append(part_response[0])
        offers.append(part_response[1])
        request.session['offer1'] = offers[0]
        request.session['offer2'] = offers[1]
        request.session['offer3'] = offers[2]
        return JsonResponse({'data': response, })
    return JsonResponse({})
