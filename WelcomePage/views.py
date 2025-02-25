from django.shortcuts import render, redirect

from .forms import TicketForm
from UserManagement.models import Student, Parent, Teacher

# Define a view for home page
def home_view(request):
    # Check if the request is a POST request (form submission)
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            new_ticket = form.save(commit=False) # Populate the form with the data from the request
            new_ticket.user = request.user
            new_ticket.save()
            return redirect('home')
    else:
        form = TicketForm()

    if request.user.is_authenticated:
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

        return render(request, 'MenuPage.html', {'form': form})

    return render(request, 'WelcomePage.html', {'form': form})
