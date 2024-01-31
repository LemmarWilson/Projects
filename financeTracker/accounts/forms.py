from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    """
    Custom user registration form.

    """

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "role", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Exclude the "ADMIN" role from choices
        self.fields['role'].choices = [(role, label) for role, label in User.Role.choices if role != 'ADMIN']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]


class UserDeleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []
