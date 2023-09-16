from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment_date = models.DateField()
    # other fields...


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    # other fields...


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    number_of_children = models.IntegerField()
    # other fields...
