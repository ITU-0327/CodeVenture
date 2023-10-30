from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import ProgressTracker

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from urllib.parse import quote


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
