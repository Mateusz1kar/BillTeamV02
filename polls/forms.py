from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from polls import models
from django.contrib.auth.models import User

from polls.models import Person ,Notification


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


class NotificationAdd(forms.ModelForm):
    what = forms.CharField(max_length=30, required=True, help_text='Optional.')
    #projectOwner = forms.CharField(max_length=30, required=False, help_text='Optional.')
    projectOwner = forms.NumberInput()
    start_date = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M',])
    edn_date = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M',])

    class Meta():
        model = Notification
        fields = ('what','projectOwner','start_date','edn_date')


# class NotificationProjectId(forms.ModelForm):
#
#     projectOwner = forms.NumberInput(required=True)
#
#     class Meta():
#         #model = Notification
#         fields = ('projectOwner')



