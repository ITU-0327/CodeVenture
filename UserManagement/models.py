from django.db import models
from django.contrib.auth.models import User
from LearningResource.models import Badge, LearningModule


class Student(models.Model):
    EXPERIENCE_CHOICES = [
        ('No experience', 'No experience'),
        ('Little experience', 'Little experience'),
        ('Comfortable', 'Comfortable'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField()
    coding_experience = models.CharField(
        max_length=20,
        choices=EXPERIENCE_CHOICES,
        default='No experience'
    )
    parent_email = models.EmailField()
    parent = models.ForeignKey('Parent', related_name='children', on_delete=models.SET_NULL, null=True, blank=True)

    teacher_email = models.EmailField()
    completed_modules = models.ManyToManyField(LearningModule)
    progress_tracker = models.OneToOneField(ProgressTracker, null=True, blank=True, on_delete=models.SET_NULL)
    module_progress = models.ManyToManyField(ModuleProgress, related_name='students')


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ManyToManyField(LearningModule)


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class ModuleProgress(models.Model):
    student = models.ForeignKey('Student', related_name='module_progress', on_delete=models.CASCADE)
    module = models.ForeignKey(LearningModule, related_name='student_progress', on_delete=models.CASCADE)
    progress_bar = models.FloatField(default=0.0)


class ProgressTracker(models.Model):
    student = models.OneToOneField('Student', on_delete=models.CASCADE)
    overall_progress_bar = models.FloatField(default=0.0)
    badges = models.ManyToManyField(Badge)
