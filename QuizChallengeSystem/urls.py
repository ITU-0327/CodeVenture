from django.urls import path

from .views import quiz_view, quiz_result_view, modules_list_quiz, quiz_list, quiz_summary_view,start_new_attempt, challenge_view, challenge_run_code, challenges_list_view

urlpatterns = [
    path('<int:quiz_id>/', quiz_view, name='quiz_view'),
    path('results/<int:result_id>/', quiz_result_view, name='quiz_result'),
    path('modules/', modules_list_quiz, name='modules_list_quiz'),
    path('concept_modules/<int:module_id>/', quiz_list, name='quiz_list'),
    path('quiz_summary/<int:quiz_id>/', quiz_summary_view, name='quiz_summary'),
    path('<int:sub_module_id>/', start_new_attempt, name='start_new_attempt'),
    path('challenge/<int:challenge_id>/', challenge_view, name='challenge'),
    path('challenge/run_code/', challenge_run_code, name='challenge_run_code'),
    path('challenge/', challenges_list_view, name='challenges_list')
]
