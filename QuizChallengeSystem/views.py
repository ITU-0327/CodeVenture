from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max
from django.utils import timezone

from LearningResource.models import LearningModule, SubModule
from .models import Quiz, Question, UserAnswer, Choice, QuizResult
from .forms import QuizForm
from django.contrib.auth.decorators import login_required
from itertools import zip_longest

from UserManagement.models import Student


@login_required
def quiz_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    if request.method == 'POST':
        form = QuizForm(request.POST, questions=questions)
        if form.is_valid():
            total_questions = len(questions)
            score = 0
            quiz_result = QuizResult.objects.create(
                quiz=quiz,
                user=request.user.student,
                score=0,
                total_questions=total_questions
            )

            for question in questions:
                selected_answer_id = form.cleaned_data.get(f"question_{question.id}")
                selected_answer_text = Choice.objects.get(id=selected_answer_id).text
                is_correct_answer = False

                try:
                    correct_choice = question.choices.get(is_correct=True)
                    if correct_choice.text == selected_answer_text:
                        is_correct_answer = True
                        score += 1
                except Choice.DoesNotExist:
                    pass

                UserAnswer.objects.create(
                    quiz_result=quiz_result,
                    question=question,
                    selected_answer=selected_answer_text,
                    is_correct=is_correct_answer
                )

            quiz_result.score = score
            quiz_result.save()

            return redirect('quiz_result', result_id=quiz_result.id)

    else:
        form = QuizForm(questions=questions)

    return render(request, 'quiz.html', {'quiz': quiz, 'form': form})


@login_required
def quiz_result_view(request, result_id):
    quiz_result = get_object_or_404(QuizResult, id=result_id)
    student = Student.objects.get(user=request.user)

    if quiz_result.user != student:
        return render(request, 'quiz_result.html', {'error': 'Quiz result does not belong to the current user'})

    user_answers = quiz_result.user_answers.all()

    total_questions = quiz_result.total_questions
    score = quiz_result.score

    results = []
    less_than_40 = 0
    between_40_and_80 = 0

    for answer in user_answers:
        choices = [
            {
                'text': f"{chr(65 + index)}) {choice.text}",
                'is_correct': choice.is_correct
            }
            for index, choice in enumerate(answer.question.choices.all())
        ]

        # Identify the selected answer's index and prefix it
        selected_answer_index = next(
            (index for index, choice in enumerate(answer.question.choices.all()) if
             choice.text == answer.selected_answer),
            None)
        selected_answer = f"{chr(65 + selected_answer_index)}) {answer.selected_answer}" if selected_answer_index is not None else answer.selected_answer

        results.append({
            'question': answer.question.text,
            'answer': selected_answer,
            'is_correct': answer.is_correct,
            'choices': choices
        })

    if score < (total_questions * 0.4):
        less_than_40 = (total_questions * 0.4)
    elif score < (total_questions * 0.8):
        between_40_and_80 = (total_questions * 0.8)

    context = {
        'score': score,
        'total_questions': total_questions,
        'results': results,
        'less_than_40': less_than_40,
        'between_40_and_80': between_40_and_80,
        'quiz': quiz_result.quiz
    }

    return render(request, 'quiz_result.html', context)


def modules_list_quiz(request):
    concept_modules = LearningModule.objects.exclude(name="Basic Modules").all()

    grouped_module = list(zip_longest(*[iter(concept_modules)] * 3))

    context = {
        'grouped_module': grouped_module
    }

    return render(request, 'module_list_quiz.html', context)


def quiz_list(request, module_id):
    module = get_object_or_404(LearningModule, id=module_id)
    sub_modules = module.sub_modules.all()

    context = {
        'module': module,
        'sub_modules': sub_modules,
    }
    return render(request, 'quiz_list.html', context)


def quiz_summary_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    student = Student.objects.get(user=request.user)
    attempts = QuizResult.objects.filter(user=student, quiz=quiz)
    now = timezone.now()
    if not attempts.exists() and quiz.deadline > now:
        return redirect('start_new_attempt', quiz_id)

    module = quiz.sub_module.parent_module
    best_score = attempts.aggregate(Max('score'))['score__max']
    context = {
        'attempts': attempts,
        'quiz': quiz,
        'module': module,
        'best_score': best_score,
        'now': now
    }

    return render(request, 'quiz_summary.html', context)


def start_new_attempt(request, sub_module_id):
    sub_modules = get_object_or_404(SubModule, id=sub_module_id)
    quiz = get_object_or_404(Quiz, id=sub_module_id)

    context = {
        'sub_modules': sub_modules,
        'quiz': quiz
    }
    # Redirect the user to the quiz page to begin the new attempt
    return render(request, 'quiz.html', context)
