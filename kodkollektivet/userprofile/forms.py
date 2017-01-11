from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """A form that creates a user, with no priviledges.
    from email and password."""

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        del self.fields['first_name']

    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserCreationForm):
    """A form that changes a user, with no priviledges.
    from email and password."""

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        del self.fields['first_name']

    class Meta:
        model = CustomUser
