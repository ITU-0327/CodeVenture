from django.urls import path

from .views import quiz_view, quiz_results

urlpatterns = [
    path('<int:quiz_id>/', quiz_view, name='quiz_view'),
    path('results/<int:quiz_id>/', quiz_results, name='quiz_results'),
]
