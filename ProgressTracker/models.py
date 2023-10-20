from django.db import models
from LearningResource.models import Badge, SubModule, LearningModule
from UserManagement.models import Student


class ProgressTracker(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    overall_progress = models.FloatField(default=0.0)
    badges = models.ManyToManyField(Badge)

    def __str__(self):
        return f"{self.student.user.username} - {self.overall_progress * 100:.2f}%"

    def update_overall_progress(self):
        total_modules = self.module_progress.count()
        total_progress = sum([mp.progress for mp in self.module_progress.all()])

        if total_modules:
            self.overall_progress = total_progress / total_modules
        else:
            self.overall_progress = 0
        self.save()


class ModuleProgress(models.Model):
    progress_tracker = models.ForeignKey(ProgressTracker, related_name='module_progress', on_delete=models.CASCADE)
    module = models.ForeignKey(LearningModule, related_name='student_progress', on_delete=models.CASCADE)
    completed_submodules = models.ManyToManyField(SubModule)
    progress = models.FloatField(default=0.0)

    def is_completed(self):
        return self.progress == 1

    def __str__(self):
        return f"{self.progress_tracker.student.user.username} - {self.module.name}"

    def update_progress(self):
        total_submodules = self.module.sub_modules.count()
        completed_submodules_count = self.completed_submodules.count()

        if total_submodules:
            self.progress = completed_submodules_count / total_submodules
        else:
            self.progress = 0
        self.save()
