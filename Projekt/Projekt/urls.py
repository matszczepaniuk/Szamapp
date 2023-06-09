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

from Szamapp.views import UserLoginView, index, RegistrationView, UserAccountView, AppStep1View, AppStep2View, \
    AppStep3View, AppStep4View, chat, Ajax

urlpatterns = [
    path('', index, name='index'),
    path("admin/", admin.site.urls),
    path("", include('theme_soft_design.urls')),
    path('chat/', chat, name='chat'),
    path('ajax/', Ajax, name='ajax'),
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("account/", UserAccountView.as_view(), name="account"),
    path("step1/", AppStep1View.as_view(), name="step1"),
    path("step2/", AppStep2View.as_view(), name="step2"),
    path("step3/", AppStep3View.as_view(), name="step3"),
    path("step4/", AppStep4View.as_view(), name="step4")
]
