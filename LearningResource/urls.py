from django.urls import path

from .views import lecture_view, basic_module_menu_view, concept_module_menu_view, concept_module_view, module_handler

urlpatterns = [
    path('', module_handler, name='module_handler'),
    path('lecture/<int:submodule_id>/', lecture_view, name='lecture_view'),
    path('basic_module/', basic_module_menu_view, name='learning_modules'),
    path('concept_module/', concept_module_menu_view, name='concept_modules'),
    path('concept_module/<int:module_id>/', concept_module_view, name='concept_module'),
   ]
