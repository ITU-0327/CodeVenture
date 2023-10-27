from django.urls import path

from .views import quiz_view, quiz_result_view, modules_list, concept_module_detail, quiz_summary_view,start_new_attempt

urlpatterns = [
    path('<int:quiz_id>/', quiz_view, name='quiz_view'),
    path('results/<int:result_id>/', quiz_result_view, name='quiz_result'),
    path('modules/', modules_list, name='modules_list'),
    path('concept_modules/<int:concept_module_id>/', concept_module_detail, name='concept_module_detail'),
    path('quiz_summary/<int:quiz_id>/', quiz_summary_view, name='quiz_summary'),
    path('<int:sub_module_id>/', start_new_attempt, name='start_new_attempt'),
]
