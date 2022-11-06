from cProfile import Profile
from django.shortcuts import render, redirect
from .forms import ProfileForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from projects.utils import searchItems, specific
from .forms import CustomUserCreateForm, ProjectForm, CommentForm
from django.views import generic
from django.contrib.auth.forms import UserChangeForm
from .models import Projects
from .models import Details, Projects, Review, Tag, Item, Color, Material, Fit
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from twilio.rest import Client
from django.db.models import Q
from django.db.models import F
from projects.filters import ColorFilter
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User

def profiles(request):
    return render(request, 'profiles.html')

class SignUp(CreateView):
    success_url = reverse_lazy("login")
    template_name = 'registration/registration.html'
    form_class = CustomUserCreateForm
    def get_absolute_url(self):
        return ('men')


@login_required(login_url='login')
def cartView(request):
    return render(request, 'cart.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
  context = {"login_view": "active"}
  if request.method == "POST":
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      return redirect("sale")
    else:
      return HttpResponse("invalid credentials")
  return render(request, "registration/login.html", context)
    

def menCatalog(request):
    item, search_query, color, material, fit, itemAll, myFilter, details, paginator = searchItems(request)
    context = {'search_query':search_query,'item':item,'myFilter':myFilter, 'itemAll':itemAll,'color':color,'fit':fit,'material':material, "paginator":paginator }
    return render(request, 'men.html', context,)

def menCatalogSpecific(request, type):
    item, search_query, color, material, fit, itemAll, myFilter, details, paginator = specific(request, type)
    context = {'search_query':search_query,'item':item,'myFilter':myFilter, 'itemAll':itemAll,'color':color,'fit':fit,'material':material, "paginator":paginator }
    return render(request, 'men.html', context,)

def womenCatalogSpecific(request, type):
    item, search_query, color, material, fit, itemAll, myFilter, details, paginator = specific(request, type)
    context = {'search_query':search_query,'item':item,'myFilter':myFilter, 'itemAll':itemAll,'color':color,'fit':fit,'material':material, "paginator":paginator }
    return render(request, 'women.html', context,)

def kidsCatalogSpecific(request, type):
    item, search_query, color, material, fit, itemAll, myFilter, details, paginator = specific(request, type)
    context = {'search_query':search_query,'item':item,'myFilter':myFilter, 'itemAll':itemAll,'color':color,'fit':fit,'material':material, "paginator":paginator }
    return render(request, 'kids.html', context,)

def saleCatalog(request):
    item, search_query, color, material, fit, itemAll, myFilter, details, paginator = searchItems(request)
    context = {'search_query':search_query,'item':item,'myFilter':myFilter, 'itemAll':itemAll,'color':color,'fit':fit,'material':material, "paginator":paginator }
    return render(request, 'sale.html', context)

def kidsCatalog(request):
    item, search_query, color, material, fit, itemAll, myFilter, details, paginator = searchItems(request)
    context = {'search_query':search_query,'item':item,'myFilter':myFilter, 'itemAll':itemAll,'color':color,'fit':fit,'material':material, "paginator":paginator }
    return render(request, 'kids.html', context)


def womenCatalog(request):
    item, search_query, color, material, fit, itemAll, myFilter, details, paginator = searchItems(request)
    context = {'search_query':search_query,'item':item,'myFilter':myFilter, 'itemAll':itemAll,'color':color,'fit':fit,'material':material, "paginator":paginator }
    return render(request, 'women.html', context,)


def project(request, object):
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        review = form.save()
        review.item = Item.objects.get(item_name=object)
        review.owner = request.user
        review.save()
    

    review = Review.objects.all()
    item, search_query, color, material, fit, itemAll, myFilter, details, paginator = searchItems(request)
    context = {'review':review,'search_query':search_query,'item':item,'myFilter':myFilter,'details':details, 'itemAll':itemAll,'color':color,'fit':fit,'material':material, 'object':object, 'form':form }
    return render(request, 'single-project.html', context)

def createProject(request):
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {'form': form}
    return render(request, "projects/project_forms.html", context)

def updateProject(request, pk):
    project = Projects.objects.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES,  instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {'form': form}
    return render(request, "projects/project_forms.html", context)

def deleteProject(request, pk):
    project = Projects.objects.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect('projects')
    context = {'object':project}
    return render(request, 'projects/delete_object.html', context)


def userAccount(request):
    context = {"user":request.user}
    return render(request, 'accounts.html', context)

def accountDetails(request):
    context = {'user':request.user}
    return render(request, 'registration/account-details.html', context)


def editAccount(request):
    user = request.user
    form = ProfileForm(instance=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST,  instance=user)
        if form.is_valid():
            form.save()
            return redirect('men')
    context = {'form':form}
    return render(request, 'registration/updateuser.html', context)