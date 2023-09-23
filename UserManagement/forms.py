from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student, Parent, Teacher


class BasicRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


class StudentCreationForm(forms.ModelForm):
    birthday = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    coding_experience = forms.ChoiceField(choices=Student.EXPERIENCE_CHOICES)
    parent_email = forms.EmailField(required=False)

    class Meta:
        model = Student
        fields = ('birthday', 'coding_experience', 'parent_email')


class ParentCreationForm(forms.ModelForm):
    children_email = forms.EmailField(required=False)

    class Meta:
        model = Parent
        fields = ('children_email',)
