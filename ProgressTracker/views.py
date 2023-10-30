from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import ProgressTracker

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
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

    response = HttpResponse(content_type='application/pdf')
    filename = f"progress_report_{progress_tracker.student.full_name()}.pdf"
    encoded_filename = quote(filename)
    response['Content-Disposition'] = f'attachment; filename="{encoded_filename}"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    def estimate_module_space(module):
        base_space = 85
        submodules_space = len(module.completed_submodules.all()) * 25
        return base_space + submodules_space

    def check_space(y_offset, space_required):
        if height - y_offset <= space_required:
            p.showPage()
            y_offset = 80
            p.setFont("Helvetica", 16)
        return y_offset

    p.setFont("Helvetica-Bold", 24)
    p.drawString(100, height - 80, f"Progress Report for {progress_tracker.student.full_name()}")

    p.setFont("Helvetica", 16)
    p.drawString(100, height - 150, f"Overall Progress: {data['overall_progress'] * 100:.2f}%")

    y_offset = 190

    for module in data['modules_progress']:
        space_required = estimate_module_space(module)
        y_offset = check_space(y_offset, space_required)
        y_offset = check_space(y_offset, 100)

        p.setFont("Helvetica-Bold", 18)
        p.drawString(100, height - y_offset, f"Module: {module.module.name}")
        y_offset += 30

        p.setFont("Helvetica", 16)
        p.drawString(100, height - y_offset, f"Progress: {module.progress * 100:.2f}%")
        y_offset += 30

        p.drawString(100, height - y_offset, "Completed Submodules:")
        y_offset += 25

        for submodule in module.completed_submodules.all():
            p.setFont("Helvetica", 14)
            p.drawString(120, height - y_offset, f"• {submodule.name}")
            y_offset += 25

        y_offset += 15

    p.showPage()
    p.save()

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