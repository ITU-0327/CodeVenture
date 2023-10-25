from django.contrib import admin
from django.urls import path, include
from WelcomePage.views import home_view
from UserManagement.views import login_view, logoutUser

urlpatterns = [
    path('admin/',      admin.site.urls),
    path('accounts/',   include('allauth.urls')),

    path('',            home_view, name="home"),
    path('login/',      login_view, name='login'),
    path('logout/',     logoutUser, name='logout'),

    path('register/',   include('UserManagement.urls')),
    path('learning/',   include('LearningResource.urls')),
    path('quiz/',       include('QuizChallengeSystem.urls')),
    path('playground/', include('PythonPlayground.urls')),
]
