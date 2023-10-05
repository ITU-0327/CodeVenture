from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required

from .forms import SubModuleForm, LearningModuleForm
from .models import SubModule


@login_required(login_url='/login/')
def create_view(request, model_type):
    if not (hasattr(request.user, 'teacher') or request.user.is_staff):
        return HttpResponse("You are not allowed here!!")

    form_class = SubModuleForm if model_type == 'submodule' else LearningModuleForm
    form = form_class(request.POST or None)

    if form.is_valid():
        form.save()

    context = {
        'form': form
    }
    return render(request, 'create.html', context)


@login_required(login_url='/login/')
def lecture_view(request, submodule_id):
    try:
        submodule = SubModule.objects.get(pk=submodule_id)
        context = {
            'submodule': submodule
        }
        return render(request, 'lecture_page.html', context)

    except SubModule.DoesNotExist:
        raise Http404("Submodule not found")


@login_required(login_url='/login/')
def lecture_view(request, submodule_id):
    try:
        submodule = SubModule.objects.get(pk=submodule_id)
        context = {
            'submodule': submodule
        }
        # return render(request, 'lecture_page.html', context)
        return render(request, 'Submodules.html', context)

    except SubModule.DoesNotExist:
        raise Http404("Submodule not found")


def challenge_quiz_view(request):
    return render(request, 'challenge_and_quiz.html')


def module_view(request):
    return render(request, 'BasicModulesPage.html')


def concept_module_view(request):
    return render(request, 'ConceptModulesPage.html')
