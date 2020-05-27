from django import forms
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.forms import UserCreationForm
from catalog.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = AuthUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']

        if email and AuthUser.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email address is already in use.')
        return email

    def save(self,commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']

        if commit:
            user.save()
            add = User(username=user.username, first_name=user.first_name, last_name=user.last_name, email=user.email)
            add.save()
        
        return user