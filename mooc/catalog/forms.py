from django import forms
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from catalog.models import User

class EditProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = AuthUser
        fields = [
            'first_name',
            'last_name',
            'email'
            ]

