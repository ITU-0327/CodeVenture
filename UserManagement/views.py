from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from .models import Student, Teacher, Parent
from .forms import StudentCreationForm, ParentCreationForm, BasicRegistrationForm

'''This function handles login and redirection.'''
def login_view(request):
    page = 'login'
    # Check if the user is already authenticated and redirect to the home page.
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            # Ensure both username and password are provided.
            messages.error(request, 'Both username and password must be provided.')
            return render(request, 'login_register.html', {'page': page})

        try:
            # Check if the user exists.
            User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')
            return render(request, 'login_register.html', {'page': page})

        user = authenticate(request, username=username, password=password)
        if user:
            # If authentication is successful, log in and redirect to the home page.
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password wrong.')
    context = {'page': page}
    return render(request, 'login_register.html', context)


def logout_user(request):
    # Log out the user and redirect to the home page.
    storage = messages.get_messages(request)
    for _ in storage:
        pass
    storage.used = True
    logout(request)
    return redirect('home')


def register_user(request, user_type=None):
    # Register a new user based on the user type (student, parent, teacher).
    if user_type not in ['student', 'parent', 'teacher']:
        raise Http404("User Type not found")

    form = BasicRegistrationForm()

    if request.method == 'POST':
        form = BasicRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            if user_type == 'student':
                # Create a Student instance for the user.
                Student.objects.create(user=user)
            elif user_type == 'parent':
                # Create a Parent instance for the user.
                Parent.objects.create(user=user)
            elif user_type == 'teacher':
                # Create a Teacher instance for the user.
                Teacher.objects.create(user=user)

            login(request, user)
            return redirect('complete_profile')

    return render(request, 'login_register.html', {'form': form, 'user_type': user_type})


@login_required(login_url='/login/')
def complete_profile(request):
    # Allow users to fill in their profiles based on their role (student, parent).
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
                # Update Student information with form data.
                user.student.birthday = form.cleaned_data.get('birthday')
                user.student.coding_experience = form.cleaned_data.get('coding_experience')
                user.student.parent_email = form.cleaned_data.get('parent_email', None)
                user.student.profile_completed = True

                parent_email = form.cleaned_data.get('parent_email', None)
                if parent_email:
                    try:
                        # Link the student to a parent if the parent's email is provided.
                        parent = Parent.objects.get(user__email=parent_email)
                        user.student.parent = parent
                    except ObjectDoesNotExist:
                        messages.error(request, f'No parent found with the email: {parent_email}')

                user.student.save()

            elif user_type == 'parent':
                user.parent.profile_completed = True
                children_email = form.cleaned_data.get('children_email')
                try:
                    # Link the parent to a student based on the child's email.
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


''' This function allows the user to choose their role (student, parent, teacher) if not already set.'''
def choose_user_type(request):
    # Allow users to choose their role (student, parent, teacher) if not already set.
    if request.method != 'POST':
        return render(request, 'SelectRoleForm.html')

    selected_role = request.POST.get('role')
    if not request.user.is_authenticated:
        return redirect('register_user', user_type=selected_role)

    if hasattr(request.user, 'student'):
        request.user.student.delete()
    if hasattr(request.user, 'parent'):
        request.user.parent.delete()
    if hasattr(request.user, 'teacher'):
        request.user.teacher.delete()

    if selected_role == 'student':
        Student.objects.get_or_create(user=request.user)
        return redirect('complete_profile')
    elif selected_role == 'parent':
        Parent.objects.get_or_create(user=request.user)
        return redirect('complete_profile')
    elif selected_role == 'teacher':
        Teacher.objects.get_or_create(user=request.user)
        return redirect('home')

