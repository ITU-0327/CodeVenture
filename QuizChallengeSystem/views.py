from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max
from django.utils import timezone

# import for run challenge code
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import base64
import requests
import time

from LearningResource.models import LearningModule, SubModule
from .models import Quiz, Question, UserAnswer, Choice, QuizResult, Challenge
from .forms import QuizForm
from django.contrib.auth.decorators import login_required
from itertools import zip_longest

from UserManagement.models import Student

SUCCESS = 3
WRONG_ANSWER = 4
RUN_TIME_ERROR = 11


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


def challenge_view(request, challenge_id):
    print(challenge_id)
    challenge = Challenge.objects.get(id=challenge_id)
    context = {
        "challenge": challenge
    }
    return render(request, 'challenge.html', context)


@csrf_exempt
def challenge_run_code(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        code = body_data.get('code', '')
        challenge_id = body_data.get('challenge_id', '')

        print(code)

        encoded_code = base64.b64encode(code.encode()).decode('utf-8')
        challenge = Challenge.objects.get(id=challenge_id)

        stdin = challenge.std_in.encode().decode('unicode_escape')
        stdin = base64.b64encode(stdin.encode()).decode('utf-8')

        expected_output = challenge.expected_output.encode().decode('unicode_escape')

        url = "https://judge0-ce.p.rapidapi.com/submissions/"

        querystring = {"base64_encoded": "true", "wait": "false", "fields": "*"}

        payload = {
            "language_id": 71,
            "source_code": encoded_code,
            "redirect_stderr_to_stdout": True,
            "stdin": stdin,
            "expected_output": expected_output
        }

        headers = {
            "content-type": "application/json",
            "Content-Type": "application/json",
            "X-RapidAPI-Key": "4488a01de2msh7b39afb80b4a53dp1f0172jsndd17e06649b3",
            "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com"
        }

        response = requests.post(url, json=payload, headers=headers, params=querystring)

        token = response.json().get('token')

        time.sleep(2)

        url = f"https://judge0-ce.p.rapidapi.com/submissions/{token}"

        querystring = {"base64_encoded": "true", "fields": "*"}

        headers = {
            "X-RapidAPI-Key": "4488a01de2msh7b39afb80b4a53dp1f0172jsndd17e06649b3",
            "X-RapidAPI-Host": "judge0-ce.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        response_data = response.json()
        status_id = response_data.get('status_id')

        max_retries = 10
        retry_count = 0

        while status_id != 3 and retry_count < max_retries:
            time.sleep(0.1)
            response = requests.get(url, headers=headers, params=querystring)
            response_data = response.json()
            status_id = response_data.get('status_id')
            retry_count += 1

        if status_id in [SUCCESS, WRONG_ANSWER, RUN_TIME_ERROR]:
            decoded_output = base64.b64decode(response_data.get('stdout', '')).decode('utf-8')
            context = {
                'stdout': decoded_output,
                'result': False if status_id in [WRONG_ANSWER, RUN_TIME_ERROR] else True,
                'expected_output': base64.b64decode(response_data.get('expected_output', '')).decode('utf-8') if status_id == WRONG_ANSWER else None
            }
            return JsonResponse(context)
        else:
            return JsonResponse({'error': 'Execution took too long or another error occurred.'})

    return JsonResponse({'error': 'Only POST method is supported.'})


def challenges_list_view(request):
    challenges = Challenge.objects.all()
    return render(request, 'challenge_list.html', {'challenges': challenges})
