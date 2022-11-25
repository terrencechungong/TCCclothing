from django.contrib import admin
from .models import  Review, Tag, Item, Color, Details, Material, Sale, Fit, CartItem, Purchase

# Register your models here.
admin.site.register(Review)
admin.site.register(Tag)
admin.site.register(Item)
admin.site.register(Color)
admin.site.register(Details)
admin.site.register(Material)
admin.site.register(Sale)
admin.site.register(Fit)
admin.site.register(CartItem)
admin.site.register(Purchase)

