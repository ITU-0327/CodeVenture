from django.db import models
from UserManagement.models import Student
from LearningResource.models import SubModule
import uuid


class Challenge(models.Model):
    # Model for representing coding challenges.
    name = models.CharField(max_length=50)
    description = models.TextField()  # A detailed description of the coding challenge.
    hints = models.TextField()
    solution_code = models.TextField()  # The expected solution code.
    std_in = models.TextField(null=True, blank=True)  # Standard input for the challenge (optional).
    expected_output = models.TextField(null=True, blank=True)
    sample_output = models.TextField(null=True, blank=True)  # Sample output for the challenge (optional).


class Quiz(models.Model):
    # Model for representing quizzes.
    name = models.CharField(max_length=50)
    deadline = models.DateTimeField(null=True, blank=True)  # Deadline for the quiz (optional).

    sub_module = models.OneToOneField(SubModule, null=True, on_delete=models.CASCADE, related_name='quiz')

    def __str__(self):
        return self.name  # Return the name as the string representation of the quiz.


class Question(models.Model):
    # Model for representing quiz questions.
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)  # Link to the parent quiz.
    text = models.TextField()
    points = models.IntegerField(default=1)  # Points associated with the question, default is 1.

    def __str__(self):
        return str(self.quiz) + ' - ' + self.text  # Return a string representation of the question.


class Choice(models.Model):
    # Model for representing answer choices in quiz questions.
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)  #Link to the parent question.
    text = models.CharField(max_length=200)  # The text of the answer choice.
    is_correct = models.BooleanField(default=False)  # Indicates if the choice is correct or not.


class QuizResult(models.Model):
    # Model for storing quiz results.
    session_id = models.UUIDField(default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz_result')  # Link to the parent quiz.
    user = models.ForeignKey(Student, on_delete=models.CASCADE)  # Link to the user who took the quiz.
    score = models.IntegerField()
    total_questions = models.IntegerField()  # Total number of questions in the quiz.
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the result was created.

class UserAnswer(models.Model):
    # Model for storing user answers to quiz questions.
    quiz_result = models.ForeignKey(QuizResult, related_name='user_answers', null=True, on_delete=models.SET_NULL)  # Link to the parent quiz result.
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # Link to the question.
    selected_answer = models.CharField(max_length=100)  # The answer selected by the user.
    is_correct = models.BooleanField(default=False)
