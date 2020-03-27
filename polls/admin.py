from django.contrib import admin
from .models import  Project, Person, Notification
# Register your models here.

admin.site.register(Person)
admin.site.register(Project)
admin.site.register(Notification)