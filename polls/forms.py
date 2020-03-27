from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from polls import models
from django.contrib.auth.models import User

from polls.models import Person as Person


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'last_name','first_name','email')


class UserProfileInfoForm(forms.ModelForm):
    position = forms.CharField(max_length=30, required=False, help_text='Optional.')
    admin = forms.BooleanField(required=False, help_text='Optional.')
    class Meta():
        model = Person
        fields = ('position', 'admin')


