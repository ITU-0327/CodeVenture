from django.shortcuts import render, redirect, get_object_or_404
from .models import Quiz, Question, UserAnswer
from .forms import QuizForm
from django.contrib.auth.decorators import login_required


@login_required
def quiz_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    if request.method == 'POST':
        form = QuizForm(request.POST, questions=questions)
        if form.is_valid():
            for question in questions:
                UserAnswer.objects.create(
                    user=request.user.student,
                    question=question,
                    selected_answer=form.cleaned_data.get(f"question_{question.id}")
                )
            return redirect('quiz_results', quiz_id=quiz_id)

    else:
        form = QuizForm(questions=questions)

    return render(request, 'quiz.html', {'quiz': quiz, 'form': form})

