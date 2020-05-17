from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from polls import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.dateparse import parse_datetime

from polls.models import Person ,Notification, Project


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'last_name','first_name','email')

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class UserProfileInfoForm(forms.ModelForm):
    position = forms.CharField(max_length=30, required=False, help_text='Optional.')
    admin = forms.BooleanField(required=False, help_text='Optional.')
    class Meta():
        model = Person
        fields = ('position', 'admin')


class NotificationAdd(forms.ModelForm):
    what = forms.CharField(max_length=30, required=True)
    #projectOwner = forms.CharField(max_length=30, required=False, help_text='Optional.')

    projectOwner = forms.NumberInput()

    start_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M',])
    end_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M',])



    #start_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])

    #end_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])



    class Meta():
        model = Notification
        fields = ('what','projectOwner','start_date','end_date')
        labels = {'projectOwner': 'Project name'}

class projektadd(forms.ModelForm):

    name = forms.CharField(max_length=50, required=True)
    description = forms.CharField(max_length=50, required=True)
    owner = forms.NumberInput()
    state = forms.CharField(max_length=50, required=True)

    class Meta():
        model = Project
        fields = ('name','description','owner','state')
        labels = {'name': 'Project Name',
                  'description': 'Description',
                  'owner': 'Owner',
                  'state': 'Actual state'}
# class NotificationProjectId(forms.ModelForm):
#
#     projectOwner = forms.NumberInput(required=True)
#
#     class Meta():
#         #model = Notification
#         fields = ('projectOwner')



