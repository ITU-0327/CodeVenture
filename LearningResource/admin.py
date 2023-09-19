from django.contrib import admin

from .models import SubModule, LearningModule, VideoTutorial

admin.site.register(SubModule)
admin.site.register(LearningModule)
admin.site.register(VideoTutorial)
