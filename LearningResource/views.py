from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from itertools import zip_longest

from .forms import SubModuleForm, LearningModuleForm
from .models import SubModule, LearningModule

from ProgressTracker.models import ProgressTracker, ModuleProgress
from UserManagement.models import Student
from QuizChallengeSystem.models import Quiz


@login_required(login_url='/login/')
def lecture_view(request, submodule_id):
    submodule = get_object_or_404(SubModule, id=submodule_id)
    module = SubModule.parent_module

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

                if not completed_submodule.next_submodule:
                    return redirect('module_handler')

            except SubModule.DoesNotExist:
                raise Http404("Completed submodule not found")

        context = {
            'submodule': submodule,
            'module': module
        }
        return render(request, 'Submodules.html', context)

    except SubModule.DoesNotExist:
        raise Http404("Submodule not found")


@login_required(login_url='/login/')
def basic_module_menu_view(request):
    student = Student.objects.get(user=request.user)
    progress_tracker = ProgressTracker.objects.get(student=student)

    basic_module = LearningModule.objects.get(name="Basic Modules")

    module_progress = ModuleProgress.objects.get(
        progress_tracker=progress_tracker,
        module=basic_module
    )

    context = {
        'module_progress': module_progress
    }
    return render(request, 'BasicModulesPage.html', context)


@login_required(login_url='/login/')
def concept_module_menu_view(request):
    student = Student.objects.get(user=request.user)
    progress_tracker = ProgressTracker.objects.get(student=student)

    all_modules = LearningModule.objects.all()
    user_module_progresses = progress_tracker.module_progress.all()

    module_progresses_with_dummies = []
    module_count = len(all_modules) - 1  # Don't count the Basic Modules
    finished_count = 0

    for module in all_modules:
        if module.name == "Basic Modules":
            continue

        user_progress = user_module_progresses.filter(module=module).first()

        if user_progress:
            module_progresses_with_dummies.append(user_progress)

            if user_progress.is_completed():
                finished_count += 1

        else:
            dummy_progress = ModuleProgress(module=module, progress=0)
            module_progresses_with_dummies.append(dummy_progress)

    grouped_module_progresses = list(zip_longest(*[iter(module_progresses_with_dummies)] * 3))

    context = {
        'grouped_module_progresses': grouped_module_progresses,
        'module_count': module_count,
        'finished_count': finished_count
    }
    return render(request, 'ConceptModulesPage.html', context)


@login_required(login_url='/login/')
def concept_module_view(request, module_id):
    module = get_object_or_404(LearningModule, id=module_id)
    if module.name == "Basic Modules":
        return redirect('learning_modules')
    student = Student.objects.get(user=request.user)
    progress_tracker = ProgressTracker.objects.get(student=student)
    module_progress, create = ModuleProgress.objects.get_or_create(progress_tracker=progress_tracker, module=module)
    sub_modules = module.sub_modules.all()

    context = {
        'module': module,
        'module_progress': module_progress,
        'sub_modules': sub_modules,
    }
    return render(request, 'ConceptModule.html', context)


@login_required(login_url='/login/')
def module_handler(request):
    student = Student.objects.get(user=request.user)
    progress_tracker = ProgressTracker.objects.get(student=student)

    basic_module = LearningModule.objects.get(name="Basic Modules")

    module_progress, created = ModuleProgress.objects.get_or_create(
        progress_tracker=progress_tracker,
        module=basic_module
    )

    if module_progress.is_completed():
        return redirect('concept_modules')

    return redirect('learning_modules')


