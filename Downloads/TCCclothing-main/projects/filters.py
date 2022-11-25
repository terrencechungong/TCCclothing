import django_filters
from .models import *
from django_filters import NumberFilter

class ColorFilter(django_filters.FilterSet):
     price_gt = NumberFilter(field_name="price", lookup_expr="gte")
     price_lt = NumberFilter(field_name="price", lookup_expr="lte")
     class Meta:
         model = Item
         fields = ['color', 'on_sale', 'fit', 'material']