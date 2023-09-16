from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        user.first_name = sociallogin.account.extra_data['given_name']
        user.last_name = sociallogin.account.extra_data['family_name']
        user.save()
        return user
