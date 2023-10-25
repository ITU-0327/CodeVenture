from django.urls import path

from .views import register_user, choose_user_type, complete_profile

urlpatterns = [
    path('user/<str:user_type>', register_user, name='register_user'),
    path('choose_user_type/', choose_user_type, name='choose_user_type'),
    path('complete_profile/', complete_profile, name='complete_profile'),
]
