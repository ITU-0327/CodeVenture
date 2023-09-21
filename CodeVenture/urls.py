"""
URL configuration for CodeVenture project.

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
from django.urls import path, include
from WelcomePage.views import home_view
from LearningResource.views import create_view, lecture_view, challenge_quiz_view, module_view
from UserManagement.views import login_view, logoutUser, register_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),

    path('', home_view, name="home"),

    path('login/', login_view, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('register/', register_user, name='register'),


    path('create/<str:model_type>/', create_view, name='create_view'),
    path('lecture/<int:submodule_id>/', lecture_view, name='lecture_view'),

    path('challenge_quiz/', challenge_quiz_view, name='challenges_quizzes'),
    path('module/', module_view, name='learning_modules'),
]
