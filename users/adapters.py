from allauth.account.adapter import DefaultAccountAdapter


class UserAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        user.name = data.get('name')
        user.lastname = data.get('lastname')
        user.save()
        return user