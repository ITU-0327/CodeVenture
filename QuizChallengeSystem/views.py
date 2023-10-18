from django.shortcuts import render, redirect, get_object_or_404
from .models import Quiz, Question, UserAnswer, Choice, QuizResult
from .forms import QuizForm
from django.contrib.auth.decorators import login_required

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

            return redirect('quiz_results', quiz_id=quiz_id)

    else:
        form = QuizForm(questions=questions)

    return render(request, 'quiz.html', {'quiz': quiz, 'form': form})


@login_required
def quiz_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    student = Student.objects.get(user=request.user)

    latest_quiz_result = QuizResult.objects.filter(user=student, quiz=quiz).latest('created_at')
    if latest_quiz_result is None:
        return render(request, 'quiz_results.html', {'error': 'No quiz results found'})

    user_answers = latest_quiz_result.user_answers.all()

    total_questions = quiz.questions.count()
    score = latest_quiz_result.score

    results = []
    for answer in user_answers:
        results.append({
            'question': answer.question.text,
            'answer': selected_answer,
            'is_correct': answer.is_correct,
            'choices': choices
        })

    return render(request, 'quiz_results.html', {
        'score': score,
        'total_questions': total_questions,
        'results': results
    })
