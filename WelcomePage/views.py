from django.shortcuts import render, redirect

from .forms import TicketForm
from UserManagement.models import Student, Parent, Teacher


def home_view(request):
    if request.user.is_authenticated:
        try:
            profile = None
            profile_completed = False

            if hasattr(request.user, 'student'):
                profile = request.user.student
                profile_completed = profile.profile_completed
            elif hasattr(request.user, 'parent'):
                profile = request.user.parent
                profile_completed = profile.profile_completed
            elif hasattr(request.user, 'teacher'):
                profile_completed = True

            if not request.user.is_staff and not profile_completed:
                return redirect('choose_user_type')

        except Exception as e:
            print("An error occurred:", e)
            return redirect('choose_user_type')

    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            new_ticket = form.save(commit=False)
            new_ticket.user = request.user
            new_ticket.save()
            return redirect('home')
    else:
        form = TicketForm()

    return render(request, 'base_generic.html', {'form': form})
