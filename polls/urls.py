
from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views #logowanie
app_name = 'polls'

urlpatterns = [
    path('',views.index,name='index'),
    path('PersonList/', views.PersonList.as_view(), name='personList'),
    path('DetailPerson/<int:pk>/', views.DetailPerson.as_view(), name='detailPerson'),
    # ex: /polls/5/results/
   # path('detailProject/<int:idProject>/', views.detailProject, name='detailProject'),
    # ex: /polls/5/vote/
   # path('detailNotification/<int:idNotification>/', views.detailNotification, name='detailNotification'),
    path('PersonFormExecute/', views.personFormExecute, name='personFormExecute'),
    path('PersonFormDeleteExecute/', views.personFormDeleteExecute, name='personDelee'),
    path('AddPersonFormExecute/', views.addPersonFormExecute, name='personAdd'),

    path('ProjectList/', views.ProjectList.as_view(), name='projectList'),

    #url(r'^register/$', views.register, name='register'),
    #url(r'^login/$', auth_views.LoginView, name='login'),
    #url(r'^logout/$', auth_views.auth_logout, name='logout'),


    path('login/', views.login_handmade, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('Register/', views.register, name='register'),
]


