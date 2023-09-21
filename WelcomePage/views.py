from django.shortcuts import render, redirect

from .forms import TicketForm


def home_view(request):
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
    # return render(request, 'index.html')
