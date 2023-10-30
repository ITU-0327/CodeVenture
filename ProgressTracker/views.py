from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string
from .models import ProgressTracker
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

    html_string = render_to_string('progress_report_template.html', {'data': data})

    # Convert to PDF
    pdf = HTML(string=html_string).write_pdf()

    # Create response
    response = HttpResponse(pdf, content_type='application/pdf')
    filename = f"progress_report_{progress_tracker.student.full_name()}.pdf"
    encoded_filename = quote(filename)
    response['Content-Disposition'] = f'attachment; filename="{encoded_filename}"'

    return response
