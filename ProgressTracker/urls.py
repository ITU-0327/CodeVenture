from django.urls import path
from .views import download_report

urlpatterns = [
    path('download_report/<int:student_id>/', download_report, name='download_report'),
]
