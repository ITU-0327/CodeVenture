from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from .models import Student, Teacher, Parent
from .forms import StudentCreationForm, ParentCreationForm, BasicRegistrationForm


def login_view(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Both username and password must be provided.')
            return render(request, 'login_register.html', {'page': page})

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
            return render(request, 'login_register.html', {'page': page})

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password wrong.')
    context = {'page': page}
    return render(request, 'login_register.html', context)


def logoutUser(request):
    storage = messages.get_messages(request)
    for _ in storage:
        pass
    storage.used = True
    logout(request)
    return redirect('home')


def register_user(request, user_type=None):
    if user_type not in ['student', 'parent', 'teacher']:
        raise Http404("User Type not found")

    form = BasicRegistrationForm()

    if request.method == 'POST':
        form = BasicRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            if user_type == 'student':
                Student.objects.create(user=user)
            elif user_type == 'parent':
                Parent.objects.create(user=user)
            elif user_type == 'teacher':
                Teacher.objects.create(user=user)

            login(request, user)
            return redirect('complete_profile')

    return render(request, 'login_register.html', {'form': form, 'user_type': user_type})


@login_required(login_url='/login/')
def complete_profile(request):
    user = request.user

    if hasattr(user, 'student'):
        form_class = StudentCreationForm
        user_type = 'student'
    elif hasattr(user, 'parent'):
        form_class = ParentCreationForm
        user_type = 'parent'
    elif hasattr(user, 'teacher'):
        return redirect('home')
    else:
        return redirect('choose_user_type')

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            if user_type == 'student':
                user.student.birthday = form.cleaned_data.get('birthday')
                user.student.coding_experience = form.cleaned_data.get('coding_experience')
                user.student.parent_email = form.cleaned_data.get('parent_email', None)
                user.student.profile_completed = True

                parent_email = form.cleaned_data.get('parent_email', None)
                if parent_email:
                    try:
                        parent = Parent.objects.get(user__email=parent_email)
                        user.student.parent = parent
                    except ObjectDoesNotExist:
                        messages.error(request, f'No parent found with the email: {parent_email}')

                user.student.save()

            elif user_type == 'parent':
                user.parent.profile_completed = True
                children_email = form.cleaned_data.get('children_email')
                try:
                    student = Student.objects.get(user__email=children_email)
                    student.parent = user.parent
                    student.save()
                except ObjectDoesNotExist:
                    messages.error(request, f'No student found with the email: {children_email}')

                user.parent.save()

            return redirect('home')
    else:
        form = form_class()

    return render(request, 'login_register.html', {'form': form})


def choose_user_type(request):
    print("Entered choose_user_type function")  # Debug line
    if request.method == 'POST':
        selected_role = request.POST.get('role')
        print(f"Selected role: {selected_role}")  # Debug line
        if request.user.is_authenticated:
            print("User is authenticated")  # Debug line
            if hasattr(request.user, 'student'):
                request.user.student.delete()
            if hasattr(request.user, 'parent'):
                request.user.parent.delete()
            if hasattr(request.user, 'teacher'):
                request.user.teacher.delete()
            print("Deleted old roles if any")  # Debug line

            if selected_role == 'student':
                Student.objects.get_or_create(user=request.user)
                print("Redirecting to complete profile for student")  # Debug line
                return redirect('complete_profile')
            elif selected_role == 'parent':
                Parent.objects.get_or_create(user=request.user)
                print("Redirecting to complete profile for parent")  # Debug line
                return redirect('complete_profile')
            elif selected_role == 'teacher':
                Teacher.objects.get_or_create(user=request.user)
                print("Redirecting to home for teacher")  # Debug line
                return redirect('home')

        else:
            print("User is not authenticated")  # Debug line
            return redirect('register_user', user_type=selected_role)
    return render(request, 'SelectRoleForm.html')
