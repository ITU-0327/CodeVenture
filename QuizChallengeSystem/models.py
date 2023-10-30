from django.db import models
from UserManagement.models import Student
from LearningResource.models import SubModule
import uuid


class Challenge(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    hints = models.TextField()
    solution_code = models.TextField()
    std_in = models.TextField(null=True, blank=True)
    expected_output = models.TextField(null=True, blank=True)
    sample_output = models.TextField(null=True, blank=True)


class Quiz(models.Model):
    name = models.CharField(max_length=50)
    deadline = models.DateTimeField(null=True, blank=True)

    sub_module = models.OneToOneField(SubModule, null=True, on_delete=models.CASCADE, related_name='quiz')

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    points = models.IntegerField(default=1)

    def __str__(self):
        return str(self.quiz) + ' - ' + self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)


class QuizResult(models.Model):
    session_id = models.UUIDField(default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz_result')
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class UserAnswer(models.Model):
    quiz_result = models.ForeignKey(QuizResult, related_name='user_answers', null=True, on_delete=models.SET_NULL)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)
