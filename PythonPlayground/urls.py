from django.urls import path

from .views import playground_view, run_code

urlpatterns = [
    path('', playground_view, name='playground'),
    path('run_code/', run_code, name='run_code'),
]
