from django.db import models
from django.contrib.auth.models import User
from LearningResource.models import Badge, SubModule


class ModuleProgress(models.Model):
    student = models.ForeignKey('Student', related_name='progress', on_delete=models.CASCADE)
    module = models.ForeignKey(SubModule, related_name='student_progress', on_delete=models.CASCADE)
    progress_bar = models.FloatField(default=0.0)

    def is_completed(self):
        return self.progress_bar == 1

    def __str__(self):
        return self.student.user.username + ' - ' + self.module.name


class ProgressTracker(models.Model):
    student = models.OneToOneField('Student', on_delete=models.CASCADE)
    overall_progress_bar = models.FloatField(default=0.0)
    completed_modules = models.ManyToManyField(SubModule)
    badges = models.ManyToManyField(Badge)

    def __str__(self):
        return self.student.user.username + ' - ' + self.overall_progress_bar * 100 + '%'


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

    progress_tracker = models.OneToOneField(ProgressTracker, null=True, blank=True, on_delete=models.SET_NULL, related_name='student_entry')
    module_progress = models.ManyToManyField(ModuleProgress, related_name='students')

    profile_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ManyToManyField(SubModule)

    def get_students(self):
        teacher_modules = self.course.all()
        enrolled_students = Student.objects.filter(completed_modules__in=teacher_modules).distinct()
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
