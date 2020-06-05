
from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views #logowanie
app_name = 'polls'

urlpatterns = [
    path('',views.index,name='index'),
    path('PersonList/', views.PersonList, name='personList'),
    # path('PersonListK/', views.PersonListKieownik.as_view(), name='personListKierownik'),
    path('DetailPerson/<int:pk>/', views.DetailPerson, name='detailPerson'),
    # path('DetailPersonK/<int:pk>/', views.DetailPersonKierownik.as_view(), name='detailPersonKierownik'),
    # ex: /polls/5/results/
    path('DetailProject/<int:pk>/', views.DetailProject.as_view(), name='detailProject'),   #nie dzziała
    # ex: /polls/5/vote/
   # path('detailNotification/<int:idNotification>/', views.detailNotification, name='detailNotification'),
    path('PersonFormExecute/', views.personFormExecute, name='personFormExecute'),
    path('PersonFormDeleteExecute/', views.personFormDeleteExecute, name='personDelee'),
    path('AddPersonFormExecute/', views.addPersonFormExecute, name='personAdd'),

    path('ProjectList/', views.ProjectList.as_view(), name='projectList'),
    path('ProjectListK/', views.ProjectListKieronik.as_view(), name='projectListKierownik'),
    path('ProjektUsun/', views.ProjectDelExecute, name='projectDel'),

    #url(r'^register/$', views.register, name='register'),
    #url(r'^login/$', auth_views.LoginView, name='login'),
    #url(r'^logout/$', auth_views.auth_logout, name='logout'),


    path('login/', views.login_handmade, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('Register/', views.register, name='register'),
    path('Notifikation/', views.NotifikationForm, name='notifikationSend'),
    path('NotifikationUser/', views.NotifikationUser, name='notifikationUser'),
    path('NotifikationFormDeleteExecute/', views.notifikationFormDeleteExecute, name='notifikationDelee'),
    path('ProjectAdd/', views.projectadd, name='AddProject'),
    path('ProjectAddAdmin/', views.projectadd, name='AddProjectAdmin'),
    path('Start/', views.SartPage, name='startpage'),

    path('NotifikationProject/', views.NotifikationProject, name='notifikationProject'),
    path('Raport/', views.EndMonthRaport, name='raportMont'),
    path('RaportProjekt/', views.EndMonthProjectRaport, name='raportProject'),

    path('WyslijDoZatwierdzenia/', views.EndMonhRequest, name='endMontRequest'),
    path('Zatwierdz/', views.EndMonth, name='endMonth'),
    path('CofnijZatwierdzenie/', views.delEndMonhRequest, name='delEndMontReques'),

    path('MojeProjekty/', views.ProjectUserOwner, name='ProjectOwned')

]


