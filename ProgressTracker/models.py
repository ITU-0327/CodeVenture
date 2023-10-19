from django.db import models
from LearningResource.models import Badge, SubModule, LearningModule
from UserManagement.models import Student


class ModuleProgress(models.Model):
    progress_tracker = models.ForeignKey('ProgressTracker', related_name='module_progress', on_delete=models.CASCADE)
    module = models.ForeignKey(LearningModule, related_name='student_progress', on_delete=models.CASCADE)
    completed_submodules = models.ManyToManyField(SubModule)
    progress = models.FloatField(default=0.0)

    def is_completed(self):
        return self.progress == 1

    def __str__(self):
        return self.student.user.username + ' - ' + self.module.name


class ProgressTracker(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    overall_progres = models.FloatField(default=0.0)
    badges = models.ManyToManyField(Badge)

    def __str__(self):
        return self.student.user.username + ' - ' + self.overall_progress * 100 + '%'
