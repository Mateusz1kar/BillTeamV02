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
    first_name = forms.CharField(max_length=30, required=False, help_text='Opcjonalne.', label="Imie")
    last_name = forms.CharField(max_length=30, required=False, help_text='Opcjonalne', label="Nazwisko")
    email = forms.EmailField(max_length=254, help_text='Wymagane',label="E-Mail")


    class Meta:
        model = User
        fields = ('username', 'email','first_name','last_name', 'password1', 'password2')
        labels = {
            "username": "Login"
        }

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class UserProfileInfoForm(forms.ModelForm):
    position = forms.CharField(max_length=30, required=False, help_text='Opcjonalnie')
    admin = forms.BooleanField(required=False, )

    class Meta():
        model = Person
        fields = ('position', 'admin')


class NotificationAdd(forms.ModelForm):
    what = forms.CharField(max_length=30, required=True, label="Opis")
    #projectOwner = forms.CharField(max_length=30, required=False, help_text='Optional.')

    projectOwner = forms.NumberInput()


    start_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M'],label="Czas rozpoczęcia")
    edn_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M'],label="Czas zakończenia")




    #start_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])

    #end_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])



    class Meta():
        model = Notification
        # fields = ('what','projectOwner','start_date','edn_date')
        # labels = {'projectOwner': 'Project name',
        #           'edn_date':'End date'}
        fields = ('projectOwner','what','start_date','edn_date')
        labels = {'projectOwner': 'Projekt',
                  'edn_date':'Czas zakończenia'}

class projektadd(forms.ModelForm):

    name = forms.CharField(max_length=50, required=True, label="Nazwa Projektu")
    description = forms.CharField(max_length=50, required=True, label="Opis")
    owner = forms.NumberInput()
    #state = forms.CharField(max_length=50, required=True,label="Status projektu")

    class Meta():
        model = Project
        fields = ('name','description','owner')#,'state')
        labels = {'owner': 'Kierownik projektu'}
# class NotificationProjectId(forms.ModelForm):
#
#     projectOwner = forms.NumberInput(required=True)
#
#     class Meta():
#         #model = Notification
#         fields = ('projectOwner')



