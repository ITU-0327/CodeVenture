from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required

from .forms import SubModuleForm, LearningModuleForm
from .models import SubModule

from ProgressTracker.models import ProgressTracker, ModuleProgress


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

        if request.GET.get('complete_current'):
            progress_tracker = ProgressTracker.objects.get(student__user=request.user)
            module_progress, created = ModuleProgress.objects.get_or_create(
                progress_tracker=progress_tracker,
                module=submodule.parent_module
            )

            module_progress.add_completed_submodule(submodule)

        context = {
            'submodule': submodule
        }
        return render(request, 'Submodules.html', context)

    except SubModule.DoesNotExist:
        raise Http404("Submodule not found")


def module_view(request):
    return render(request, 'BasicModulesPage.html')


def concept_module_view(request):
    return render(request, 'ConceptModulesPage.html')
