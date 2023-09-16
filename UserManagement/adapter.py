from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import Student, Teacher, Parent


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)

        user.first_name = sociallogin.account.extra_data['given_name']
        user.last_name = sociallogin.account.extra_data['family_name']

        # Create user type based on some criteria
        user_type = request.POST.get('user_type', 'student')  # This could be passed in a hidden field in the form
        if user_type == 'student':
            Student.objects.create(user=user, enrollment_date=...)
        elif user_type == 'teacher':
            Teacher.objects.create(user=user, subject=...)
        elif user_type == 'parent':
            Parent.objects.create(user=user, number_of_children=...)

        user.save()
        return user
