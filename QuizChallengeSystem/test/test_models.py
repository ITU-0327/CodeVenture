import pytest
from datetime import datetime
from QuizChallengeSystem.models import Quiz, Question


# Fixtures
@pytest.fixture
def quiz():
    return Quiz.objects.create(name='Test Quiz')


@pytest.fixture
def question(quiz):
    return Question.objects.create(quiz=quiz, text='Sample Question', points=1)


# Test
@pytest.mark.django_db
def test_quiz_str_representation(quiz):
    assert str(quiz) == 'Test Quiz'


@pytest.mark.django_db
def test_question_str_representation(question, quiz):
    expected_str = str(quiz) + ' - ' + 'Sample Question'
    assert str(question) == expected_str
