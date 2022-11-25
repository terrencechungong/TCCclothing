from cProfile import Profile
from django.shortcuts import render, redirect
from .forms import CartAddForm, ProfileForm
import locale
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from projects.utils import searchItems, specific, sale
from .forms import CustomUserCreateForm, CommentForm, PurchaseForm
from django.views import generic
from django.contrib.auth.forms import UserChangeForm
from .models import Details, Review, Tag, Item, Color, Material, Fit, CartItem, Purchase
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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
    total = 0
    cartSize = 0
    cartIds = ""
    cartItems = CartItem.objects.filter(purchased="False")
    for i in cartItems:
        types = i.quantity
        if i.cartOwner == request.user:
            if i.itemInCart.on_sale.sale_name == "On Sale":
                total += (i.itemInCart.price * .6)*i.quantity
                cartSize += 1
                cartIds += (str(i.id)+" ")
            else:
                total += (i.itemInCart.price)*i.quantity
                cartSize += 1
                cartIds += (str(i.id)+" ")
    totalf = "{:.2f}".format(total)
    cartIds = cartIds[:len(cartIds)-1]
    context = {'cartItems':cartItems,'total':totalf,'cartSize':cartSize,'cartIds':cartIds}
    return render(request, 'cart.html', context)


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
      return redirect("men")
    else:
      return HttpResponse("invalid credentials")
  return render(request, "registration/login.html", context)
    
@login_required(login_url='login')
def menCatalog(request):
    item, search_query, color, material, fit, itemAll, myFilter, details, paginator = searchItems(request)
    context = {'search_query':search_query,'item':item,'myFilter':myFilter, 'itemAll':itemAll,'color':color,'fit':fit,'material':material, "paginator":paginator }
    return render(request, 'men.html', context,)

@login_required(login_url='login')
def menCatalogSpecific(request, type):
    item, search_query, color, material, fit, itemAll, myFilter, details, paginator = specific(request, type)
    context = {'search_query':search_query,'item':item,'myFilter':myFilter, 'itemAll':itemAll,'color':color,'fit':fit,'material':material, "paginator":paginator }
    return render(request, 'men.html', context,)

@login_required(login_url='login')
def womenCatalogSpecific(request, type):
    item, search_query, color, material, fit, itemAll, myFilter, details, paginator = specific(request, type)
    item = Item.objects.filter(type=str(type)).annotate(prod=F('price')*.6)
    context = {'search_query':search_query,'item':item,'myFilter':myFilter, 'itemAll':itemAll,'color':color,'fit':fit,'material':material, "paginator":paginator }
    return render(request, 'women.html', context,)

@login_required(login_url='login')
def kidsCatalogSpecific(request, type):
    item, search_query, color, material, fit, itemAll, myFilter, details, paginator = specific(request, type)
    context = {'search_query':search_query,'item':item,'myFilter':myFilter, 'itemAll':itemAll,'color':color,'fit':fit,'material':material, "paginator":paginator }
    return render(request, 'kids.html', context,)

@login_required(login_url='login')
def saleCatalog(request, gender):
    item, search_query, color, material, fit, itemAll, myFilter, details, paginator = sale(request, gender)
    context = {'search_query':search_query,'item':item,'myFilter':myFilter, 'itemAll':itemAll,'color':color,'fit':fit,'material':material, "paginator":paginator,'gender':gender }
    return render(request, 'sale.html', context)

@login_required(login_url='login')
def kidsCatalog(request):
    item, search_query, color, material, fit, itemAll, myFilter, details, paginator = searchItems(request)
    context = {'search_query':search_query,'item':item,'myFilter':myFilter, 'itemAll':itemAll,'color':color,'fit':fit,'material':material, "paginator":paginator }
    return render(request, 'kids.html', context)

@login_required(login_url='login')
def womenCatalog(request):
    item, search_query, color, material, fit, itemAll, myFilter, details, paginator = searchItems(request)
    context = {'search_query':search_query,'item':item,'myFilter':myFilter, 'itemAll':itemAll,'color':color,'fit':fit,'material':material, "paginator":paginator }
    return render(request, 'women.html', context,)

@login_required(login_url='login')
def project(request, id):
    # show price on the single project view
    form2 = CartAddForm()
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        review = form.save()
        review.item = Item.objects.get(id=id)
        review.owner = request.user
        review.save()
    revLen = 0
    review = Review.objects.all()
    for rev in review:
        if rev.item == Item.objects.get(id=id):
            revLen += 1
    item, search_query, color, material, fit, itemAll, myFilter, details, paginator = searchItems(request)
    item = Item.objects.get(id=id)
    context = {'revLen':revLen,'form2':form2,'review':review,'search_query':search_query,'i':item,'myFilter':myFilter,'details':details, 'itemAll':itemAll,'color':color,'fit':fit,'material':material, 'object':object, 'form':form }
    return render(request, 'single-project.html', context)

@login_required(login_url='login')
def addToCartView(request, item):
    # make it so that if the item they are sdding to the cart already exists it
    # just updates the quantity
    #create an equals method
    cartitems = CartItem.objects.all()
    form = CartAddForm()
    if request.method == "POST":
        form = CartAddForm(request.POST)
        cartitem = form.save()
        cartitem.save()
        return redirect('project', item)




def AddCartItem(request, pk):
    # make buttons smaller and add an option addToCartViewsubract from the cart
    cartitem = CartItem.objects.get(id=pk)
    form = CartAddForm(instance=cartitem)
    if request.method == "POST":
        form = CartAddForm(request.POST, request.FILES,  instance=cartitem)
        if form.is_valid():
            cartitem.quantity += 1
            form.save()
            return redirect('cart')


def DeleteCartItem(request, pk):
    # make buttons smaller and add an option addToCartViewsubract from the cart
    cartitem = CartItem.objects.get(id=pk)
    form = CartAddForm(instance=cartitem)
    if request.method == "POST":
        form = CartAddForm(request.POST, request.FILES,  instance=cartitem)
        if form.is_valid():
            cartitem.quantity -= 1
            form.save()
        if cartitem.quantity == 0:
            cartitem.delete()
        return redirect('cart')

def userAccount(request):
    context = {"user":request.user}
    return render(request, 'accounts.html', context)

def accountDetails(request):
    cartitem = CartItem.objects.filter(purchased="True")
    # remove store credit and make that an order section thT SHOWS 2
    # OPTIONS AND GIVES THEM A LINK TO CLICK IF THEY 
    # WANT TO SEE ALL
    purchases = Purchase.objects.filter(purchaseOwner=request.user)
    purchaseLen = len(purchases)
    for i in range(len(purchases)):
        purchases[i].purchasedItemIds = purchases[i].purchasedItemIds.split(' ')
        purchases[i].purchasedItemIds = list(map(int, purchases[i].purchasedItemIds))
    context = {'user':request.user, 'purchases':purchases, 'purLen':purchaseLen, 'cartitem':cartitem}
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

def purchaseView(request):
    # just finish the view
    # pull all the data from the cartitem instances before delete() is called
    if request.method == "POST":
        form = PurchaseForm(request.POST)
        purchase = form.save()
        purchase.save()
        itemIds = purchase.purchasedItemIds.split(' ')
        itemIds = list(map(int, itemIds))
        for cartItemId in itemIds:
            item = CartItem.objects.get(id=cartItemId)
            item.purchased = "True"
            item.save()
        context = {'idli':itemIds}
        return render(request, 'projects/purchase.html', context)