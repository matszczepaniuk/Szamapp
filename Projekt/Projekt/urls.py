"""
URL configuration for Projekt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from Szamapp.views import userlogin, index, RegistrationView, UserAccountView, AppStep1View, AppStep2View, \
    AppStep3View, AppStep4View, ChatMealOffers, main, AppStep5View, ChatInstructions, AppStep6View, userlogout

urlpatterns = [
    path('', main, name='main'),
    path('index/', index, name='index'),
    path("admin/", admin.site.urls),
    path('index/', include('theme_soft_design.urls')),
    path('chat-meal-offers/', ChatMealOffers, name='chat_meal_offers'),
    path('ajax2/', ChatInstructions, name='ajax2'),
    path("login/", userlogin, name="login"),
    path("logout/", userlogout, name="logout"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("account/", UserAccountView.as_view(), name="account"),
    path("step1/", AppStep1View.as_view(), name="step1"),
    path("step2/", AppStep2View.as_view(), name="step2"),
    path("step3/", AppStep3View.as_view(), name="step3"),
    path("step4/", AppStep4View.as_view(), name="step4"),
    path("step5/", AppStep5View.as_view(), name="step5"),
    path("step6/", AppStep6View.as_view(), name="step6")
]
