from django.urls import path
from .views import download_report, parent_concept_modules_view

urlpatterns = [
    path('download_report/<int:student_id>/', download_report, name='download_report'),
    path('learning_module/', parent_concept_modules_view, name='parent_progress_tracker')
]
