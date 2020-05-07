from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.urls import reverse
from django.views import generic

from .models import Person, Project, Notification

#logowanie
import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.http import JsonResponse
from .forms import SignUpForm, UserProfileInfoForm , NotificationAdd
from django.contrib.auth import authenticate

# Create your views here.

class PersonList(generic.ListView):
    template_name = 'polls/person.html'
    context_object_name = 'person'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('polls:login'))
        else:
            return Person.objects.order_by('user')



def index (request):
    return HttpResponse("Hello, world. You're at the polls index.")



class  DetailPerson(generic.DetailView):
    template_name = 'polls/detailPerson.html'
    context_object_name = 'person'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('polls:login'))
        else:
            return Person.objects.order_by('idPerson')
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
        person2.position = request.POST['position']
        #pom = False
        try:
            if (request.POST['czyA']):
                pom = True
        except:
            pom = False
        person2.admin = pom

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
            'error_message': "You didn't select a choice.",
        })
    else:

        person2.delete()
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

        person2 = Person()
        #person = Person(firstName=request.POST['fname'], lastName=request.POST['lname'], login = request.POST['login'], password=request.POST['password'], position=request.POST['position'], admin= pom)

        person2.firstName = request.POST['fname']
        person2.lastName = request.POST['lname']
        person2.login = request.POST['login']
        person2.password = request.POST['password']
        person2.position = request.POST['position']
        person2.admin = pom

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
        return Project.objects.order_by('idProject')





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

    er = []

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                person = get_object_or_404(Person, user=user)
                # Redirect to a success page.
                if  person.admin:
                    return render(request, 'polls/StartAdmin.html')
                else:
                    return render(request,'polls/startUser.html')
            else:
                # Return a 'disabled account' error message
                #er.append("Twoje konto jest zablokowane")
                return render(request,'polls/login.html')
        else:
            # Return an 'invalid login' error message.
            #er.append("Bledne logowanie")
            return render(request, 'polls/login.html')

    return render(request,'polls/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('polls:login'))


def NotifikationForm(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('polls:login'))
    else:
        registered = False
        if request.method == 'POST':
            noti_form= NotificationAdd(data=request.POST)
            if noti_form.is_valid():

                notifikation = noti_form.save(commit=False)
                notifikation.who = request.user
               # notifikation.projectOwner = get_object_or_404(Project,idNotification=noti_form.data.projectOwner)
                notifikation.save()
                registered = True
            else:
                print(noti_form.errors)
        else:
            noti_form = NotificationAdd()
        czyAdmin = get_object_or_404(Person, user=request.user).admin
        if(czyAdmin ):
            return render(request, 'polls/NotifikationAdmin.html',
                          {'noti_form': noti_form,
                           'registered': registered,
                           'czyAdmin': czyAdmin})
        return render(request,'polls/notifikation.html',
                              {'noti_form':noti_form,
                               'registered':registered,
                               'czyAdmin':czyAdmin})


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
        registered = False

        if request.method == 'POST':
            return render(request, 'polls/notifikationUser.html',
                          {'notifikation': Notification.objects.filter(who=request.POST['id'])})



def notifikationFormDeleteExecute(request):
    try:
        notifikation = get_object_or_404(Notification, idNotification=request.POST['id'])

    except (KeyError, Notification):
        # Redisplay the question voting form.
        return render(request, 'polls/notifikationUser.html/'+request.user)
    else:
        person = notifikation.who
        notifikation.delete()
        return render(request, 'polls/notifikationUser.html',
                      {'notifikation': Notification.objects.filter(who=person.id)})


def SartPage(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('polls:login'))
    else:
        person = get_object_or_404(Person, user=request.user)
        if( person.admin) :
            return  render(request,'polls/StartAdmin.html')
        else:
            return  render(request,'polls/startUser.html')

