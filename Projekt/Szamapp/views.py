from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from Szamapp.forms import *
from Szamapp.models import *
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import openai
from django.conf import settings


def index(request):
    #
    return render(request, 'pages/index.html')


def main(request):
    """# Displays main page of the program"""
    if request.user.is_authenticated:
        return redirect('step1')
    else:
        return render(request, 'pages/main.html')


@csrf_protect
def userlogin(request):
    """# Logs in user, if exists"""
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('step1')
        else:
            form = UserLoginForm
            context = {
                'form': form
            }
            return render(request, 'pages/login.html', context)

    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return render(request, 'pages/login.html')
        return redirect('step1')


def userlogout(request):
    """# Logs out user, if logged in"""
    if request.user.is_authenticated:
        username = request.user.username
        if username is not None:
            logout(request)
            return redirect('main')


class RegistrationView(View):
    """# Creates user account"""
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('step1')
        else:
            form = RegistrationForm()
            context = {
                'form': form
            }
            return render(request, 'pages/registration.html', context)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password1 = form.cleaned_data.get("password1")
            password2 = form.cleaned_data.get("password2")
            email = form.cleaned_data.get("email")
            if password1 == password2:
                new_user = User.objects.create_user(username=username, email=email, password=password1)
                new_user.save()
                users_stats = AppStatistics.objects.filter(id=1)
                users_amount = int(users_stats.users)
                new_users_amount = users_amount + 1
                users_stats.update(users=new_users_amount)
                return redirect('login')
            else:
                form = RegistrationForm(request.POST)
                context = {
                    'form': form
                }
                return render(request, 'pages/registration.html', context)
        else:
            form = RegistrationForm(request.POST)
            context = {
                'form': form
            }
            return render(request, 'pages/registration.html', context)


class UserAccountView(LoginRequiredMixin, View):
    """# Displays user profile page, visible only for logged-in users"""
    def get(self, request):
        if request.user.is_authenticated:
            username = request.user.get_username()
            user = User.objects.get(username=username)
            user_id = request.user.id
            saved_recipes = FavouriteRecipes.objects.filter(user=user_id)
            return render(request, 'pages/account.html', {'saved_recipes': saved_recipes})
        else:
            return redirect('login')


class AppStep1View(View):
    """# Handles page of the program, where preparation time is being selected"""
    def get(self, request):
        form = Step1Form()
        context = {
            'form': form
        }
        return render(request, 'pages/step1.html', context)

    def post(self, request):
        form = Step1Form(request.POST)
        if form.is_valid():
            val = form.cleaned_data.get("btn")
            request.session['time'] = val
        else:
            form = Step1Form()
            context = {
                'form': form
            }
            return render(request, 'pages/step1.html', context)
        return redirect('step2')


class AppStep2View(View):
    """# Handles page of the program, where meal base is being selected"""
    def get(self, request):
        form = Step2Form()
        context = {
            'form': form
        }
        return render(request, 'pages/step2.html', context)

    def post(self, request):
        form = Step2Form(request.POST)
        if form.is_valid():
            val = form.cleaned_data.get("btn")
            request.session['base'] = val
        else:
            form = Step2Form()
            context = {
                'form': form
            }
            return render(request, 'pages/step2.html', context)
        return redirect('step3')


class AppStep3View(View):
    """# Handles page of the program, where meal type is being selected"""
    def get(self, request):
        form = Step3Form()
        context = {
            'form': form
        }
        return render(request, 'pages/step3.html', context)

    def post(self, request):
        form = Step3Form(request.POST)
        if form.is_valid():
            meal_type = form.cleaned_data.get("btn")
            request.session['type'] = meal_type
        else:
            form = Step3Form()
            context = {
                'form': form
            }
            return render(request, 'pages/step3.html', context)
        return redirect("step4")


class AppStep4View(View):
    """# Handles page of the program, where user gives preferred ingredients"""
    def get(self, request):
        form = Step4Form()
        form.ingredient1 = request.session.get('ingredient1')
        form.ingredient2 = request.session.get('ingredient2')
        form.ingredient3 = request.session.get('ingredient3')
        form.ingredient4 = request.session.get('ingredient4')
        form.ingredient5 = request.session.get('ingredient5')
        context = {
            'form': form
        }
        return render(request, 'pages/step4.html', context)

    def post(self, request):
        form = Step4Form(request.POST)
        if form.is_valid():
            ingredient_1 = form.cleaned_data.get("ingredient1")
            ingredient_2 = form.cleaned_data.get("ingredient2")
            ingredient_3 = form.cleaned_data.get("ingredient3")
            ingredient_4 = form.cleaned_data.get("ingredient4")
            ingredient_5 = form.cleaned_data.get("ingredient5")
            request.session['ingredient1'] = ingredient_1
            request.session['ingredient2'] = ingredient_2
            i1 = Ingredient.objects.create(name=ingredient_1)
            i1.save()
            i2 = Ingredient.objects.create(name=ingredient_2)
            i2.save()
            if ingredient_3 != "":
                request.session['ingredient3'] = ingredient_3
                i3 = Ingredient.objects.create(name=ingredient_3)
                i3.save()
            if ingredient_4 != "":
                request.session['ingredient4'] = ingredient_4
                i4 = Ingredient.objects.create(name=ingredient_4)
                i4.save()
            if ingredient_5 != "":
                request.session['ingredient5'] = ingredient_5
                i5 = Ingredient.objects.create(name=ingredient_5)
                i5.save()
        else:
            form = Step4Form()
            context = {
                'form': form,
                'message': 'Musisz podać dwa składniki'
            }
            return render(request, 'pages/step4.html', context)
        return ChatMealOffers(request)


class AppStep5View(View):
    """# Handles page of the program, where user select the mostly preferred meal"""
    def get(self, request):
        chat_response_meals = request.session.get('first_response')
        offers = chat_response_meals.split(".")
        meal_one = offers[1]
        first_meal = meal_one.rstrip(meal_one[-1])
        request.session['first_meal'] = first_meal
        meal_two = offers[2]
        second_meal = meal_two.rstrip(meal_two[-1])
        request.session['second_meal'] = second_meal
        third_meal = offers[3]
        request.session['third_meal'] = third_meal
        context = {
            'first_meal': first_meal,
            'second_meal': second_meal,
            'third_meal': third_meal,
        }
        return render(request, 'pages/step5.html', context)

    def post(self, request):
        if "first_meal" in request.POST:
            first_meal = request.session.get('first_meal')
            request.session['choice'] = first_meal
        elif "second_meal" in request.POST:
            second_meal = request.session.get('second_meal')
            request.session['choice'] = second_meal
        elif "third_meal" in request.POST:
            third_meal = request.session.get('third_meal')
            request.session['choice'] = third_meal
        return ChatInstructions(request)


class AppStep6View(View):
    """# Handles the last page of the program, where ingredients and instructions are being given"""
    def get(self, request):
        name = request.session.get('choice')
        recipe = request.session.get('second_response')
        context = {
            'name': name,
            'recipe': recipe,
        }
        return render(request, 'pages/step6.html', context)

    def post(self, request):
        name = request.session.get('choice')
        recipe = request.session.get('second_response')
        if "save" in request.POST:
            r = Recipe.objects.create(name=name, instructions=recipe)
            r.save()
            current_user = request.user
            current_user_id = current_user.id
            fav = FavouriteRecipes.objects.create(name=name, user=current_user_id)
            recipes_stats = AppStatistics.objects.filter(id=1)
            recipes_amount = int(recipes_stats.recipes)
            new_recipes_amount = recipes_amount + 1
            recipes_stats.update(recipes=new_recipes_amount)
            return redirect('account')
        elif "exit" in request.POST:
            return redirect('main')


@csrf_exempt
def ChatMealOffers(request):
    """# Background correspondence with Chat GPT, where 3 meal offers are being found"""
    meal_time = request.session.get('time')
    meal_base = request.session.get('base')
    meal_type = request.session.get('type')
    meal_ingredient1 = request.session.get('ingredient1')
    meal_ingredient2 = request.session.get('ingredient2')
    meal_ingredient3 = request.session.get('ingredient3')
    meal_ingredient4 = request.session.get('ingredient4')
    meal_ingredient5 = request.session.get('ingredient5')
    text = f"Wypunktuj, jako listę numerowaną 3 propozycje {meal_type} z następujących produktów: {meal_base}, " \
           f"{meal_ingredient1}, {meal_ingredient2}, {meal_ingredient3}, {meal_ingredient4}, {meal_ingredient4}, " \
           f"{meal_ingredient5}, czas przygotowania do {meal_time}, możesz dorzucić jakieś produkty od siebie, podaj " \
           f"tylko nazwy dań, na razie nie podawaj instrukcji przygotowania i listy składników"
    openai.api_key = settings.OPENAI_API_KEY
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"{text}"}
        ]
    )
    response = res.choices[0].message["content"]
    request.session['first_response'] = response
    return redirect('step5')


@csrf_exempt
def ChatInstructions(request):
    """# Background correspondence with Chat GPT, where list of ingredients and instructions are being provided"""
    selected_meal = request.session.get('choice')
    text = f"Podaj listę składników i przepis dla dania {selected_meal}"
    openai.api_key = settings.OPENAI_API_KEY
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"{text}"}
        ]
    )
    response = res.choices[0].message["content"]
    request.session['second_response'] = response
    return redirect('step6')
