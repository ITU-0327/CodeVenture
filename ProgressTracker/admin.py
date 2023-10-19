from django.contrib import admin
from .models import ModuleProgress, ProgressTracker

admin.site.register(ModuleProgress)
admin.site.register(ProgressTracker)
