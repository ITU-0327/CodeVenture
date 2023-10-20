from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required

from .forms import SubModuleForm, LearningModuleForm
from .models import SubModule

from ProgressTracker.models import ProgressTracker, ModuleProgress
from UserManagement.models import Student


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

        complete_submodule_id = request.GET.get('complete_current')
        if complete_submodule_id:
            try:
                completed_submodule = SubModule.objects.get(pk=complete_submodule_id)

                progress_tracker = ProgressTracker.objects.get(student__user=request.user)
                module_progress, created = ModuleProgress.objects.get_or_create(
                    progress_tracker=progress_tracker,
                    module=completed_submodule.parent_module
                )

                module_progress.add_completed_submodule(completed_submodule)

            except SubModule.DoesNotExist:
                pass

        context = {
            'submodule': submodule
        }
        return render(request, 'Submodules.html', context)

    except SubModule.DoesNotExist:
        raise Http404("Submodule not found")


def module_view(request):
    return render(request, 'BasicModulesPage.html')


@login_required(login_url='/login/')
def concept_module_view(request):
    student = Student.objects.get(user=request.user)
    progress_tracker = ProgressTracker.objects.get(student=student)
    module_progresses = progress_tracker.module_progress.all()

    context = {
        'module_progresses': module_progresses
    }
    return render(request, 'ConceptModulesPage.html', context)
