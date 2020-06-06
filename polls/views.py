import io

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.urls import reverse
from django.views import generic

from .models import Person, Project, Notification

#logowanie
# import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.http import JsonResponse
from .forms import SignUpForm, UserProfileInfoForm , NotificationAdd, projektadd
from django.contrib.auth import authenticate

from datetime import datetime
# Create your views here.
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.platypus  import Table,  TableStyle,  Paragraph
from reportlab.lib  import colors
from reportlab.pdfgen  import canvas
from reportlab.lib.pagesizes  import A4
from reportlab.pdfbase  import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet
from django.conf  import settings
from django.db.models import F
# class PersonList(generic.ListView):
#     template_name = 'polls/person.html'
#     context_object_name = 'person'
#
#     def get_queryset(self):
#         if not self.request.user.is_authenticated:
#             return HttpResponseRedirect(reverse('polls:login'))
#         else:
#             person = get_object_or_404(Person,user=self.request.user)
#             if person.kierownik:
#                 template_name = 'polls/kierownik/person.html'
#             return {'project':Person.objects.order_by('idPerson'),'error':""}

def PersonList(request):
    template_name = 'polls/person.html'
    context_object_name = 'person'

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('polls:login'))
    else:
        person = get_object_or_404(Person,user=request.user)
        if person.kierownik:
            template_name = 'polls/kierownik/personKierownik.html'
            return  render(request,template_name,{'person':Person.objects.order_by('id'),'error':""})
        elif person.admin:
             template_name = 'polls//person.html'
             return render(request, template_name, {'person': Person.objects.order_by('id'), 'error': ""})
        return HttpResponseRedirect(reverse('polls:startpage'))


# class PersonListKieownik(generic.ListView):
#     template_name = 'polls/kierownik/personKierownik.html'
#     context_object_name = 'person'
#
#     def get_queryset(self):
#         if not self.request.user.is_authenticated:
#             return HttpResponseRedirect(reverse('polls:login'))
#         else:
#             person = get_object_or_404(Person,user=self.request.user)
#             if person.kierownik:
#                 return Person.objects.order_by('user')
#             return ;


def index (request):
    return HttpResponse("Hello, world. You're at the polls index.")

def  DetailPerson(request,**kwargs):
    template_name = 'polls/detailPerson.html'
    context_object_name = 'person'
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('polls:login'))
    else:
        person = get_object_or_404(Person,user=request.user)
        if person.kierownik:
            template_name='polls/kierownik/detailPersonKierownik.html'
            p=get_object_or_404(Person,id=kwargs['pk'])
            return render(request, template_name, {'person':p, 'error':""})
        elif person.admin:
            template_name = 'polls//detailPerson.html'
            p = get_object_or_404(Person, id=kwargs['pk'])
            return render(request, template_name, {'person': p, 'error': ""})
        else:
            return HttpResponseRedirect(reverse('polls:startpage'))


# class  DetailPerson(generic.DetailView):
#     template_name = 'polls/detailPerson.html'
#     context_object_name = 'person'
#
#     def get_queryset(self):
#         if not self.request.user.is_authenticated:
#             return HttpResponseRedirect(reverse('polls:login'))
#         else:
#             return Person.objects.order_by('idPerson')
#
# class DetailPersonKierownik(generic.DetailView):
#         template_name = 'polls/kierownik/detailPersonKierownik.html'
#         context_object_name = 'person'
#
#         def get_queryset(self):
#             if not self.request.user.is_authenticated:
#                 return HttpResponseRedirect(reverse('polls:login'))
#             else:
#                 return Person.objects.order_by('idPerson')
    #person = Person.objects.filter(idPerson=pk).first()



    #person2 = get_object_or_404(Person, idPerson=idPerson)





def personFormExecute(request):
    try:
        person2 = get_object_or_404(Person, id=request.POST['id'])
        person2.user.first_name = request.POST['fname']
        person2.user.last_name = request.POST['lname']
        person2.user.username = request.POST['login']
        try:
            if request.POST['password']:
                person2.user.set_password(request.POST['password'])
        finally:
            ex = "nie zmieniono hasła"

        #person2.password = request.POST['password']
        # person2.position = request.POST['position']
        #pom = False
        try:
            if (request.POST['czyA']):
                pom = True
        except:
            pom = False

        try:
            if (request.POST['czyK']):
                pomK = True
        except:
            pomK = False

        person2.admin = pom
        if pom & pomK:
            person2.admin = True
            person2.kierownik = False
        else:
            person2.admin = pom
            person2.kierownik = pomK

    except (KeyError, Person):
        # Redisplay the question voting form.
        return render(request, 'polls/detailPerson.html', {
            'person': person2,
            'error_message': "You didn't select a choice.",
        })
    else:
        person2.user.save()
        person2.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:detailPerson', args=(person2.id,)))


def personFormDeleteExecute(request):
    try:
        person2 = get_object_or_404(Person, id=request.POST['id'])

    except (KeyError, Person):
        # Redisplay the question voting form.
        return render(request, 'polls/detailPerson.html', {
            'person': person2,
            'error_message': "Nie dokonałeś wyboru.",
        })
    else:
        if person2.position=="Dezaktywowany":
            date =datetime.now()
            if date.month==1 :
                date.month=13
                date.year-=1
            person2.position = ""+ (datetime(date.year,date.month-1,28)).strftime("%Y-%m")+" = Zatwierdzony"
        else:
            person2.position="Dezaktywowany"
        person2.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:personList'))

def addPersonFormExecute(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('polls:login'))
    else:
        #pom = False
        try:
            if (request.POST['czyA']):
                pom = True
        except:
            pom = False

        try:
            if (request.POST['czyK']):
                pomK = True
        except:
            pomK = False

        person2 = Person()
        #person = Person(firstName=request.POST['fname'], lastName=request.POST['lname'], login = request.POST['login'], password=request.POST['password'], position=request.POST['position'], admin= pom)

        person2.firstName = request.POST['fname']
        person2.lastName = request.POST['lname']
        person2.login = request.POST['login']
        person2.password = request.POST['password']
        # person2.position = request.POST['position']
        if pom & pomK:
            person2.admin = True
            person2.kierownik = False
        else:
            person2.admin = pom
            person2.kierownik = pomK


        person2.save()
        return HttpResponseRedirect(reverse('polls:personList'))


def detailProject(request, idProject):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('polls:login'))
    else:
        response = "You're looking at the results of question %s."
        return HttpResponse(response % idProject)

def detailNotification(request, idNotification):
    return HttpResponse("You're voting on question %s." % idNotification)




class ProjectList(generic.ListView):
    template_name = 'polls/ProjectList.html'
    context_object_name = 'project'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('polls:login'))
        else:
          return Project.objects.all()

class ProjectListKieronik(generic.ListView):
    template_name = 'polls/kierownik/ProjectListKierownik.html'
    context_object_name = 'project'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('polls:login'))
        else:
          return Project.objects.all()



def register(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('polls:login'))
    else:
        registered = False
        if request.method == 'POST':
            user_form = SignUpForm(data=request.POST)
            profile_form = UserProfileInfoForm(data=request.POST)
            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save()
                user.set_password(user.password)
                user.save()
                profile = profile_form.save(commit=False)
                if profile.admin & profile.kierownik:
                    profile.admin = True
                    profile.kierownik = False
                date = datetime.now()
                if date.month == 1:
                    date.month = 13
                    date.year -= 1
                profile.position = "" + (datetime(date.year, date.month-1, 28)).strftime("%Y-%m") + " = Zatwierdzony"
                profile.user = user
                profile.save()
                registered = True
            else:
                print(user_form.errors,profile_form.errors)
        else:
            user_form = SignUpForm()
            profile_form = UserProfileInfoForm()
        return render(request,'polls/register.html',
                              {'user_form':user_form,
                               'profile_form':profile_form,
                               'registered':registered})

def login_handmade(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)
    error=""
    er = []

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                person = get_object_or_404(Person, user=request.user)
                if person.position!="Dezaktywowany":
                    notifikationList = Notification.objects.filter(who=person.id)
                    sumHouersInMonth = 0
                    sumHouersInLastMonth = 0

                    for n in notifikationList:
                        if n.start_date.month == datetime.now().month:
                            fmt = '%d/%m/%Y %H:%M'
                            d1 = datetime.strptime(n.start_date.strftime(fmt), fmt)
                            d2 = datetime.strptime(n.edn_date.strftime(fmt), fmt)
                            sumHouersInMonth += (d2 - d1).seconds / 60 / 60  # * 24 *60 #.days
                        if n.start_date.month == datetime.now().month - 1:
                            fmt = '%d/%m/%Y %H:%M'
                            d1 = datetime.strptime(n.start_date.strftime(fmt), fmt)
                            d2 = datetime.strptime(n.edn_date.strftime(fmt), fmt)
                            sumHouersInLastMonth += (d2 - d1).seconds / 60 / 60  # * 24 *60 #.days

                    notifikationList = Notification.objects.filter(who=request.user,
                                                                   start_date__gt=datetime(datetime.now().year,
                                                                                           datetime.now().month, 1, 0, 0,
                                                                                           1)).order_by("-start_date")
                    if (person.admin):
                        return render(request, 'polls/StartAdmin.html',
                                      {'person': person,
                                       'notifikation': notifikationList,
                                       'sumHouersInMonth': sumHouersInMonth,
                                       'sumHouersInLastMonth': sumHouersInLastMonth
                                       })
                    elif person.kierownik:
                        return render(request, 'polls/kierownik/StartKierownik.html',
                                      {'person': person,
                                       'notifikation': notifikationList,
                                       'sumHouersInMonth': sumHouersInMonth,
                                       'sumHouersInLastMonth': sumHouersInLastMonth
                                       })
                    else:
                        return render(request, 'polls/startUser.html',
                                      {'person': person,
                                       'notifikation': notifikationList,
                                       'sumHouersInMonth': sumHouersInMonth,
                                       'sumHouersInLastMonth': sumHouersInLastMonth
                                       })
                else:
                    error="Konto zostało dezaktywowane prosze skontaktować się z administratorem"

            else:
                error = "Zły login lub chasło "
        else:
            error = "Nie można się zalogowac zły logoin lub hasło"

    return render(request,'polls/login.html',{'error':error})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('polls:login'))


def NotifikationForm(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('polls:login'))

    else:
        registered = False
        error = ""
        if request.method == 'POST':
            noti_form= NotificationAdd(data=request.POST)

            #projekt = get_object_or_404(Project, idProject=6)

            if (noti_form.is_valid() ):#& (projekt.state == "Aktywny")):
                person = get_object_or_404(Person,user=request.user)
                monthPom = person.position[5:7:1]
                pomCzyPrzeslanyDoZamkniecia=person.position[8:]
                # if datetime.now().month<10 : warunke="0"+datetime.now().month.__str__()
                # else :warunke= datetime.now().month.__str__()
                if monthPom == datetime.now().strftime("%m"):
                    error="Ten miesiąc został już zamknięty"
                elif( pomCzyPrzeslanyDoZamkniecia ==" = Zatwierdzony") & (monthPom == datetime.now().strftime("%m")):
                    error = "Ten miesiąc został już zamknięty"
                elif pomCzyPrzeslanyDoZamkniecia=="= Do zatwierdzenia":
                    error = "Ten miesiąc został już przesłany do zatwierdzenie nie można wykonać tej operacji"
                else:
                    notifikation = noti_form.save(commit=False)
                    notifikation.who = request.user
                   # notifikation.projectOwner = get_object_or_404(Project,idNotification=noti_form.data.projectOwner)
                    test = notifikation.projectOwner.__str__()[16]  # .related_fields# .select_related(noti_form.fields)
                    project = get_object_or_404(Project, idProject=test)
                    if(project.state=="Aktywny"):
                        notifikation.save()
                        registered = True
                    else:
                        error="Niestety ten projekt jest już zakończony"
            else:
                error="Błędne dane formularza"
        else:
            noti_form = NotificationAdd()
        person = get_object_or_404(Person, user=request.user)

        if(person.admin ):
            return render(request, 'polls/NotifikationAdmin.html',
                          {'noti_form': noti_form,
                           'registered': registered,
                           'czyAdmin': person.admin,
                           'error': error})
        elif person.kierownik:
            return render(request, 'polls/kierownik/NotifikationKierownik.html',
                          {'noti_form': noti_form,
                           'registered': registered,
                           'czyAdmin': person.admin,
                           'error': error})
        return render(request,'polls/notifikation.html',
                              {'noti_form':noti_form,
                               'registered':registered,
                               'czyAdmin':person.admin,
                                'error': error})

def EndMonth(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('polls:login'))
    else:
        if request.method == 'POST':
            person= get_object_or_404(Person,user=request.POST['idEndR'])
            monthPom = person.position[5:7:1]
            pomCzyPrzeslanyDoZamkniecia = person.position[8:]
            if person.position != "Dezaktywowany":
                if pomCzyPrzeslanyDoZamkniecia == "= Do zatwierdzenia":
                    date = datetime.now()
                    if date.month == 1:
                        date.month = 13
                        date.year -= 1
                    person.position = "" + (datetime(date.year, date.month , 28)).strftime("%Y-%m") + " = Zatwierdzony"
                    person.save()
                    if person.kierownik:
                        template_name = 'polls/kierownik/detailPersonKierownik.html'
                        return render(request, template_name, {'person': person, 'error': ""})
                    else:
                        return HttpResponseRedirect(reverse('polls:startpage'))


                else:
                    error = "Ten miesiąc nie został jeszcze przesłany do zatwierdzenie nie można wykonać tej operacji "+pomCzyPrzeslanyDoZamkniecia
            else:
                error = "Ten urzytkownik jest dezaktywowany nie można wykonac operacji"
        else:
            error = "Zła metoda dostępu"
    return render(request, 'polls/kierownik/Error.html', {'error': error})




def EndMonhRequest(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('polls:login'))
    else:
        person= get_object_or_404(Person,user=request.user)
        monthPom = person.position[5:7:1]
        pomCzyPrzeslanyDoZamkniecia = person.position[8:]
        if person.position != "Dezaktywowany":
            if pomCzyPrzeslanyDoZamkniecia != "= Do zatwierdzenia":
                date = datetime.now()
                person.position = "" + (datetime(date.year, date.month , 28)).strftime("%Y-%m") + " = Do zatwierdzenia"
                person.save()
                return HttpResponseRedirect(reverse('polls:startpage'))

            else:
                error = "Ten miesiąc już zsotał przesłany do zatwierdzenia"
        else:
            error = "Ten urzytkownik jest dezaktywowany nie można wykonac operacji"
        return render(request, 'polls/kierownik/Error.html', {'error': error})

def delEndMonhRequest(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('polls:login'))
    else:
        person= get_object_or_404(Person,user=request.user)
        monthPom = person.position[5:7:1]
        pomCzyPrzeslanyDoZamkniecia = person.position[8:]
        if person.position != "Dezaktywowany":
            if pomCzyPrzeslanyDoZamkniecia == "= Do zatwierdzenia":
                date = datetime.now()
                person.position = "" + (datetime(date.year, date.month-1 , 28)).strftime("%Y-%m") + " = Zatwierdzony"
                person.save()
                return HttpResponseRedirect(reverse('polls:startpage'))

            else:
                error = "Ten miesiąc nie zsotał przesłany do zatwierdzenia"
                if person.admin:
                    return  render(request,'polls/ErrorAdmin.html', {'error': error})
                elif person.kierownik:
                    return render(request, 'polls/kierownik/Error.html', {'error': error})
                else:
                    return render(request, 'polls/ErrorUser.html', {'error': error})
        else:
            error = "Ten urzytkownik jest dezaktywowany nie można wykonac operacji"

        return render(request, 'polls/login.html')
# class NotifikationUser(generic.ListView):
#     template_name = 'polls/notifikationUser.html'
#     context_object_name = 'notifikation'
#
#     def get_queryset(self):
#         person= get_object_or_404(Person,id=)
#         return Notification.objects.filter(who=person.user)

def NotifikationUser(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('polls:login'))
    else:
        if request.method == 'POST':
            notifikationList = Notification.objects.filter(who=request.POST['id'])
            sumHouersInMonth = 0
            sumHouersInLastMonth=0

            for n in notifikationList:
                if n.start_date.month == datetime.now().month:
                    fmt = '%d/%m/%Y %H:%M'
                    d1 = datetime.strptime(n.start_date.strftime(fmt), fmt)
                    d2 = datetime.strptime(n.edn_date.strftime(fmt), fmt)
                    sumHouersInMonth += (d2 - d1).seconds /60 /60  #* 24 *60 #.days
                if n.start_date.month == datetime.now().month - 1:
                    fmt = '%d/%m/%Y %H:%M'
                    d1 = datetime.strptime(n.start_date.strftime(fmt), fmt)
                    d2 = datetime.strptime(n.edn_date.strftime(fmt), fmt)
                    sumHouersInLastMonth += (d2 - d1).seconds / 60 / 60  # * 24 *60 #.days
        notifikationList = Notification.objects.filter(who=request.POST['id'], start_date__gt=datetime(datetime.now().year,datetime.now().month,1, 0,0,1 ) ).order_by("-start_date")

        return render(request, 'polls/notifikationUser.html',
                          {'notifikation': notifikationList,
                           'sumHouersInMonth':sumHouersInMonth,
                           'sumHouersInLastMonth':sumHouersInLastMonth
                           })



def notifikationFormDeleteExecute(request):
    try:
        notifikation = get_object_or_404(Notification, idNotification=request.POST['id'])

    except (KeyError, Notification):
        # Redisplay the question voting form.
        return render(request, 'polls/notifikationUser.html/'+request.user)
    else:
        person = notifikation.who
        notifikation.delete()
        pom=get_object_or_404(Person,user=person)
        notifikationList = Notification.objects.filter(who=pom.id)
        sumHouersInMonth = 0
        sumHouersInLastMonth = 0

        for n in notifikationList:
            if n.start_date.month == datetime.now().month:
                fmt = '%d/%m/%Y %H:%M'
                d1 = datetime.strptime(n.start_date.strftime(fmt), fmt)
                d2 = datetime.strptime(n.edn_date.strftime(fmt), fmt)
                sumHouersInMonth += (d2 - d1).seconds / 60 / 60  # * 24 *60 #.days
            if n.start_date.month == datetime.now().month - 1:
                fmt = '%d/%m/%Y %H:%M'
                d1 = datetime.strptime(n.start_date.strftime(fmt), fmt)
                d2 = datetime.strptime(n.edn_date.strftime(fmt), fmt)
                sumHouersInLastMonth += (d2 - d1).seconds / 60 / 60  # * 24 *60 #.days
        notifikationList = Notification.objects.filter(who=pom.id, start_date__gt=datetime(datetime.now().year,datetime.now().month,1, 0,0,1 ) ).order_by("-start_date")
        # if pom.admin:
        #      return render(request, 'polls/notifikationUser.html',
        #                    {'person': pom,
        #                     'notifikation': notifikationList,
        #                     'sumHouersInMonth': sumHouersInMonth.__round__(2),
        #                     'sumHouersInLastMonth': sumHouersInLastMonth.__round__(2)
        #                     })
        # el
        if(pom.kierownik):

            if request.POST['typ'] == "user":
                return render(request, 'polls/notifikationUser.html',
                              {'person': pom,
                               'notifikation': notifikationList,
                               'sumHouersInMonth': sumHouersInMonth.__round__(2),
                               'sumHouersInLastMonth': sumHouersInLastMonth.__round__(2)
                               })
            return HttpResponseRedirect(reverse('polls:startpage'))
        else:

            if (pom.admin):
                if request.POST['typ'] == "start":
                    return render(request, 'polls/StartAdmin.html',
                                  {'person': pom,
                                   'notifikation': notifikationList,
                                   'sumHouersInMonth': sumHouersInMonth.__round__(2),
                                   'sumHouersInLastMonth': sumHouersInLastMonth.__round__(2)
                                   })
                else:
                    tempalte = "polls/ProjectDetailAdmin.html"
                    return render(request, tempalte,
                              {'notifikation': Notification.objects.filter(projectOwner_id=request.POST['idP'][16]).order_by(
                                  '-start_date'),
                               'project': get_object_or_404(Project, idProject=request.POST['idP'][16])})
            else:
                if request.POST['typ'] == "projekt":
                    tempalte = "polls/ProjectDetailUser.html"
                    return render(request, tempalte,
                                  {'notifikation': Notification.objects.filter(projectOwner_id=request.POST['idP'][16]).order_by('-start_date'),
                                      'project': get_object_or_404(Project, idProject=request.POST['idP'][16])})
                return render(request, 'polls/startUser.html',
                              {'person': pom,
                               'notifikation': notifikationList,
                               'sumHouersInMonth': sumHouersInMonth.__round__(2),
                               'sumHouersInLastMonth': sumHouersInLastMonth.__round__(2)
                               })



def SartPage(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('polls:login'))
    else:
        person = get_object_or_404(Person, user=request.user)
        notifikationList = Notification.objects.filter(who=person.id).order_by("-start_date")
        sumHouersInMonth = 0
        sumHouersInLastMonth = 0


        for n in notifikationList:
            if n.start_date.month == datetime.now().month:
                fmt = '%d/%m/%Y %H:%M'
                d1 = datetime.strptime(n.start_date.strftime(fmt), fmt)
                d2 = datetime.strptime(n.edn_date.strftime(fmt), fmt)
                sumHouersInMonth += (d2 - d1).seconds / 60 / 60  # * 24 *60 #.days
            if n.start_date.month == datetime.now().month - 1:
                fmt = '%d/%m/%Y %H:%M'
                d1 = datetime.strptime(n.start_date.strftime(fmt), fmt)
                d2 = datetime.strptime(n.edn_date.strftime(fmt), fmt)
                sumHouersInLastMonth += (d2 - d1).seconds / 60 / 60  # * 24 *60 #.days

            # if n.start_date.month == datetime.now().month:
        data = datetime.now()
        notifikationList = Notification.objects.filter(who=person.id, start_date__gt=datetime(datetime.now().year,datetime.now().month,1, 0,0,1 ) ).order_by("-start_date")
        if( person.admin) :
            return render(request,'polls/StartAdmin.html',
                          {'person':person,
                           'notifikation':notifikationList,
                           'sumHouersInMonth': sumHouersInMonth.__round__(2),
                           'sumHouersInLastMonth':sumHouersInLastMonth.__round__(2),
                           'test':person.kierownik.__str__()
                           })
        elif person.kierownik:
            return render(request, 'polls/kierownik/StartKierownik.html',
                   {'person': person,
                    'notifikation': notifikationList,
                    'sumHouersInMonth': sumHouersInMonth.__round__(2),
                    'sumHouersInLastMonth': sumHouersInLastMonth.__round__(2),
                    'test': person.kierownik.__str__()})
        else:
            return render(request,'polls/startUser.html',
                          {'person':person,
                           'notifikation':notifikationList,
                           'sumHouersInMonth': sumHouersInMonth.__round__(2),
                           'sumHouersInLastMonth':sumHouersInLastMonth.__round__(2)
                           })

def projectadd(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('polls:login'))
    else:
        registered = False
        if request.method == 'POST':
            noti_form = projektadd(data=request.POST)
            if noti_form.is_valid():
                ProjectAdd = noti_form.save(commit=False)
                ProjectAdd.save()
                registered = True
            else:
                print(noti_form.errors)
        else:
            noti_form = projektadd()
        czyAdmin = get_object_or_404(Person, user=request.user).admin
        return render(request, 'polls/ProjectAddAdmin.html',
                      {'noti_form': noti_form,
                       'registered': registered,
                       'czyAdmin': czyAdmin})

def NotifikationProject(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('polls:login'))
    else:
        if request.method == 'POST':
            person = get_object_or_404(Person,user=request.user)
            if person.kierownik:
                tempalte= "polls/ProjectDetail.html"
            elif person.admin:
                tempalte = "polls/ProjectDetailAdmin.html"
            else:
                tempalte = "polls/ProjectDetailUser.html"
            return render(request, tempalte,
                {'notifikation': Notification.objects.filter(projectOwner_id=request.POST['id']).order_by('-start_date'),
                 'project': get_object_or_404(Project,idProject=request.POST['id'])})


class  DetailProject(generic.DetailView):
    template_name = 'polls/ProjectDetail.html'
    context_object_name = 'project'

    def get_queryset(self, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('polls:login'))
        else:
            return Notification.objects.order_by('idNotification')
                    #'project':Project.objects.filter(idProject=1)
# def projectList(request):
#     if not request.user.is_authenticated:
#         return HttpResponseRedirect(reverse('polls:login'))
#     else:
#         person = Person.object.get(uesr=request.user)
#         if person.admin:
#             #if request.method == 'POST':
#             return render(request, 'polls/notifikationUser.html',
#                         {'projects': Project.objects.filter(idProject=request.POST['id']).order_by('idProject')})
#         else :
#             return render(request, 'polls/startUser.html')

def ProjectDelExecute(request):
    project = get_object_or_404(Project, idProject=request.POST['idDel'])
    if  project.state=="Zakonczony":
        project.state = "Aktywny"
    else: project.state ="Zakonczony"
    project.save()
    person = get_object_or_404(Person,user=request.user)
    if person.kierownik:
        return HttpResponseRedirect(reverse('polls:projectListKierownik'))
    return HttpResponseRedirect(reverse('polls:ProjectOwned'))


def myProjectKierownikDel(request):
    project = get_object_or_404(Project, idProject=request.POST['idDel'])
    if project.state == "Zakonczony":
        project.state = "Aktywny"
    else:
        project.state = "Zakonczony"
    project.save()
    template_name = 'polls/kierownik/UserOwnedProjectListKierownik.html'
    projectList = Project.objects.filter(owner=request.user)
    return render(request,template_name,{'project':projectList})



def EndMonthRaport(request):
    if request.method =='POST':
        person = get_object_or_404(Person, user=get_object_or_404(User ,pk=request.POST['idP']))
    else:
        person = get_object_or_404(Person, user=request.user)
    notifikationList = Notification.objects.filter(who=person.id)
    sumHouersInMonth = 0
    sumHouersInLastMonth = 0

    for n in notifikationList:
        if n.start_date.month == datetime.now().month:
            fmt = '%d/%m/%Y %H:%M'
            d1 = datetime.strptime(n.start_date.strftime(fmt), fmt)
            d2 = datetime.strptime(n.edn_date.strftime(fmt), fmt)
            sumHouersInMonth += (d2 - d1).seconds / 60 / 60  # * 24 *60 #.days
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    #p.drawString(50, 800 , "")
    p.drawString(200, 800, "Raport konca miesaca")
    p.drawString(50, 750, "Imie:"+person.user.first_name)
    p.drawString(50, 700, "Nazwisko:" + person.user.last_name)
    p.drawString(50, 650, "Stanowisko:" + person.position)
    p.drawString(50, 600, "Liczba przepracowanych godzin:" + sumHouersInMonth.__round__(2).__str__())
    if sumHouersInMonth>=160:
        p.drawString(50, 600, "Liczba nadgodzin:"+(sumHouersInMonth-160).__round__(2).__str__())
    else:
        p.drawString(50, 550, "W tym nadgodzin:0" )
    p.drawString(50, 500, "Liczba godzin w poszczeulnych projektach:")
    liia =450
    for project in Project.objects.all():
        if Notification.objects.filter(who=person.id ,projectOwner=project.idProject ).count !=0:
            sumHouersInMonth=0
            for n in  Notification.objects.filter(who=person.id ,projectOwner=project.idProject ):
                if n.start_date.month == datetime.now().month:
                    fmt = '%d/%m/%Y %H:%M'
                    d1 = datetime.strptime(n.start_date.strftime(fmt), fmt)
                    d2 = datetime.strptime(n.edn_date.strftime(fmt), fmt)
                    sumHouersInMonth += (d2 - d1).seconds / 60 / 60  # * 24 *60 #.days
            if sumHouersInMonth!=0:
                p.drawString(50, liia, "    -Liczba godzin w "+project.name+":"+sumHouersInMonth.__round__(2).__str__())
                liia -= 50
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')


def EndMonthProjectRaport(request):
    if request.method == 'POST':
        project = get_object_or_404(Project, idProject=request.POST['idP'])
        notifikationList = Notification.objects.filter(projectOwner=project.idProject)
        sumHouersInMonth = 0
        sumHouers=0


        for n in notifikationList:
            fmt = '%d/%m/%Y %H:%M'
            d1 = datetime.strptime(n.start_date.strftime(fmt), fmt)
            d2 = datetime.strptime(n.edn_date.strftime(fmt), fmt)
            if n.start_date.month == datetime.now().month:
                sumHouersInMonth += (d2 - d1).seconds / 60 / 60  # * 24 *60 #.days
            sumHouers += (d2 - d1).seconds / 60 / 60  # * 24 *60 #.days
        # Create a file-like buffer to receive PDF data.
        buffer = io.BytesIO()

        # Create the PDF object, using the buffer as its "file."
        p = canvas.Canvas(buffer)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        #p.drawString(50, 800 , "")
        p.drawString(200, 800, "Raport projektu")
        p.drawString(50, 750, "Nazwa:"+project.name)
        p.drawString(50, 700, "Opis:" + project.description)
        p.drawString(50, 650, "Wlasciciel projektu:" + project.owner.first_name +" "+ project.owner.last_name)
        p.drawString(50, 600, "Liczba godzin w miesiacu:"+(sumHouersInMonth).__round__(2).__str__())
        p.drawString(50, 550, "Liczba godzin zycia projektu:"+sumHouers.__round__(2).__str__())
        p.drawString(50,500,"Czlatkowie projektu:")
        linia=450
        for per in  Person.objects.all():
            sumHouersInMonth=0
            sumHouers=0
            for n in  Notification.objects.filter(projectOwner=project.idProject,who=per.user):
                fmt = '%d/%m/%Y %H:%M'
                d1 = datetime.strptime(n.start_date.strftime(fmt), fmt)
                d2 = datetime.strptime(n.edn_date.strftime(fmt), fmt)
                if n.start_date.month == datetime.now().month:
                    sumHouersInMonth += (d2 - d1).seconds / 60 / 60  # * 24 *60 #.days
                sumHouers += (d2 - d1).seconds / 60 / 60  # * 24 *60 #.days
            if sumHouers != 0:
                p.drawString(50, linia, "-" + per.user.first_name + " " + per.user.last_name + " w tym miesiacu: " + (
                    sumHouersInMonth).__round__(2).__str__() + " lacznie :" + (sumHouers).__round__(2).__str__())
                linia -= 50
        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
def ProjectUserOwner(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('polls:login'))
    else:
        projectList = Project.objects.filter(owner=request.user)
        person = get_object_or_404(Person,user=request.user)
        if person.admin:
            return render(request, 'polls/UserOwnerProjectAdmin.html',
                          {'project': projectList})
        elif person.kierownik:
            return render(request, 'polls/kierownik/UserOwnedProjectListKierownik.html',
                          {'project': projectList})
        else:
            return render(request, 'polls/UserOwnedProjectList.html',
                          {'project': projectList})