from django.db import models
from django.contrib.auth.models import User

from LearningResource.models import LearningModule


class Student(models.Model):
    # Choices for coding experience
    EXPERIENCE_CHOICES = [
        ('No experience', 'No experience'),
        ('Little experience', 'Little experience'),
        ('Comfortable', 'Comfortable'),
    ]

    # User is linked to this Student, and if the User is deleted, the Student is deleted.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True)
    coding_experience = models.CharField(
        max_length=20,
        choices=EXPERIENCE_CHOICES,
        default='No experience'
    )
    parent_email = models.EmailField(null=True)
    # Parent relationship allows for connecting a student to a parent
    parent = models.ForeignKey('Parent', related_name='children', on_delete=models.SET_NULL, null=True, blank=True)

    # Flag to indicate if the student's profile is completed.
    profile_completed = models.BooleanField(default=False)

    def __str__(self):
        # Represent the object as the username of the associated User.
        return self.user.username

    def full_name(self):
        # Generate a full name for the Student based on their first and last name
        if self.user.first_name or self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}".strip()
        return self.user.username


class Teacher(models.Model):
    # User is linked to this Teacher, and if the User is deleted, the Teacher is deleted.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # A teacher can be associated with multiple LearningModules.
    course = models.ManyToManyField(LearningModule)

    def get_students(self):
        from ProgressTracker.models import ModuleProgress
        # Get all the LearningModules associated with this teacher.
        teacher_modules = self.course.all()
        # Find the ModuleProgress records for the enrolled modules.
        enrolled_module_progresses = ModuleProgress.objects.filter(module__in=teacher_modules)
        # Find students enrolled in these modules.
        enrolled_students = Student.objects.filter(
            progresstracker__module_progress__in=enrolled_module_progresses).distinct()
        return enrolled_students

    def __str__(self):
        # Represent the object as the username of the associated User.
        return self.user.username


class Parent(models.Model):
    # User is linked to this Parent, and if the User is deleted, the Parent is deleted.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Flag to indicate if the parent's profile is completed.
    profile_completed = models.BooleanField(default=False)

    def get_children(self):
        # Retrieve all the children associated with this parent.
        return self.children.all()

    def __str__(self):
        # Represent the object as the username of the associated User.
        return self.user.username
