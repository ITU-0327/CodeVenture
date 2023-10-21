from django.db import models
from django.contrib.auth.models import User

from LearningResource.models import LearningModule


class Student(models.Model):
    EXPERIENCE_CHOICES = [
        ('No experience', 'No experience'),
        ('Little experience', 'Little experience'),
        ('Comfortable', 'Comfortable'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True)
    coding_experience = models.CharField(
        max_length=20,
        choices=EXPERIENCE_CHOICES,
        default='No experience'
    )
    parent_email = models.EmailField(null=True)
    parent = models.ForeignKey('Parent', related_name='children', on_delete=models.SET_NULL, null=True, blank=True)

    profile_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ManyToManyField(LearningModule)

    def get_students(self):
        from ProgressTracker.models import ModuleProgress
        teacher_modules = self.course.all()
        enrolled_module_progresses = ModuleProgress.objects.filter(module__in=teacher_modules)

        enrolled_students = Student.objects.filter(
            progresstracker__module_progress__in=enrolled_module_progresses).distinct()

        return enrolled_students

    def __str__(self):
        return self.user.username


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profile_completed = models.BooleanField(default=False)

    def get_children(self):
        return self.children.all()

    def __str__(self):
        return self.user.username
