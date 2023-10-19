from django.db import models
from django.contrib.auth.models import User
from LearningResource.models import SubModule


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
