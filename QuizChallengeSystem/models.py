from django.db import models
from UserManagement.models import Student


class Challenge(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    hints = models.JSONField()
    solution_code = models.TextField()


class Quiz(models.Model):
    name = models.CharField(max_length=50)
    deadline = models.DateTimeField(null=True, blank=True)
    # is_active = models.BooleanField(default=True)  # Is this quiz currently active?


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    points = models.IntegerField(default=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)


class UserAnswer(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
