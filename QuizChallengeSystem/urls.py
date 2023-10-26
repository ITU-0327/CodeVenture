from django.urls import path

from .views import quiz_view, quiz_result_view, modules_list

urlpatterns = [
    path('<int:quiz_id>/', quiz_view, name='quiz_view'),
    path('results/<int:quiz_id>/', quiz_result_view, name='quiz_result'),
    path('modules', modules_list, name='modules_list'),
]
