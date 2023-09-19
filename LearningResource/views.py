from django.shortcuts import render

from .forms import SubModuleForm, LearningModuleForm


def create_view(request, model_type):
    form_class = SubModuleForm if model_type == 'submodule' else LearningModuleForm
    form = form_class(request.POST or None)

    if form.is_valid():
        form.save()

    context = {
        'form': form
    }
    return render(request, 'create.html', context)
