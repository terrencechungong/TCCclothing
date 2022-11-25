from .models import Item
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Details, Review, Tag, Item, Color, Material, Fit
from django.db.models import Q
from django.db.models import F
from projects.filters import ColorFilter

def searchItems(request):
    item = Item.objects.all().annotate(prod=F('price')*.6)
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        item = Item.objects.filter(Q(item_name__icontains=search_query) | Q(details__icontains=search_query)).annotate(prod=F('price')*.6)
    color = Color.objects.all()
    material = Material.objects.all()
    fit = Fit.objects.all()
    myFilter = ColorFilter(request.GET, queryset=item)
    item = myFilter.qs
    details = Details.objects.all()
    itemAll = Item.objects.all()
    page = request.GET.get('page')
    results = 6
    paginator = Paginator(item, results)
    return item, search_query, color, material, fit, itemAll, myFilter, details, paginator


def sale(request, gender):
    if gender == "None":
        item = Item.objects.filter(on_sale="b39cf317-e290-4124-ac50-69a338881f14").annotate(prod=F('price')*.6)
    else:
        item = Item.objects.filter(gender=gender, on_sale="b39cf317-e290-4124-ac50-69a338881f14").annotate(prod=F('price')*.6)
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        item = Item.objects.filter(Q(item_name__icontains=search_query) | Q(details__icontains=search_query)).annotate(prod=F('price')*.6)
    color = Color.objects.all()
    material = Material.objects.all()
    fit = Fit.objects.all()
    myFilter = ColorFilter(request.GET, queryset=item)
    item = myFilter.qs
    details = Details.objects.all()
    itemAll = Item.objects.all()
    page = request.GET.get('page')
    results = 6
    paginator = Paginator(item, results)
    return item, search_query, color, material, fit, itemAll, myFilter, details, paginator

def specific(request, type):
    item = Item.objects.filter(Q(item_name__icontains=type)|Q(type=type)).annotate(prod=F('price')*.6)
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        item = Item.objects.filter(Q(item_name__icontains=search_query) | Q(details__icontains=search_query)).annotate(prod=F('price')*.6)
    color = Color.objects.all()
    material = Material.objects.all()
    fit = Fit.objects.all()
    myFilter = ColorFilter(request.GET, queryset=item)
    item = myFilter.qs
    details = Details.objects.all()
    itemAll = Item.objects.all()
    page = request.GET.get('page')
    results = 10
    paginator = Paginator(item, results)
    try:
        item = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        item = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        item = paginator.page(page)
    return item, search_query, color, material, fit, itemAll, myFilter, details, paginator