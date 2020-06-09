from django.db import models

# Create your models here.
from django.db.models.functions import datetime
from django.forms import forms


from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=60)
    admin = models.BooleanField(default=False)
    kierownik = models.BooleanField(default=False)


class Project(models.Model):
    idProject = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    owner = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    state = models.CharField(max_length=50)


class Notification(models.Model):
    idNotification = models.AutoField(primary_key=True)
    who = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    what = models.CharField(max_length=100)
    projectOwner = models.ForeignKey(Project,on_delete=models.CASCADE)
    start_date = models.DateTimeField(
        default=timezone.now)
    edn_date = models.DateTimeField(
        default=timezone.now)


