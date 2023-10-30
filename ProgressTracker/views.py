from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string
from .models import ProgressTracker
from urllib.parse import quote
from UserManagement.models import Parent
from django.shortcuts import render, get_object_or_404
from LearningResource.models import LearningModule
from ProgressTracker.models import ModuleProgress
from itertools import zip_longest


def download_report(request, student_id):
    try:
        progress_tracker = ProgressTracker.objects.get(student_id=student_id)
        modules_progress = progress_tracker.module_progress.all()
    except ProgressTracker.DoesNotExist:
        return HttpResponse("Student not found", status=404)

    data = {
        'student': progress_tracker.student,
        'overall_progress': progress_tracker.overall_progress,
        'modules_progress': modules_progress,
    }

    html_string = render_to_string('progress_report_template.html', {'data': data})

    # Convert to PDF
    pdf = HTML(string=html_string).write_pdf()

    # Create response
    response = HttpResponse(pdf, content_type='application/pdf')
    filename = f"progress_report_{progress_tracker.student.full_name()}.pdf"
    encoded_filename = quote(filename)
    response['Content-Disposition'] = f'attachment; filename="{encoded_filename}"'

    return response


def parent_concept_modules_view(request):
    parent = Parent.objects.get(user=request.user)

    children = parent.get_children()
    children_data = []

    for child in children:
        student = child
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

        children_data.append({
            'student': student,
            'grouped_module_progresses': grouped_module_progresses,
            'module_count': module_count,
            'finished_count': finished_count,
        })

    context = {
        'children_data': children_data,
    }
    return render(request, 'parent_trakerprogress.html', context)