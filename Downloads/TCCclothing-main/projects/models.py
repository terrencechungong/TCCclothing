from xml.dom.pulldom import default_bufsize
from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver



class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)

    def __str__(self):
        return self.name


class Details(models.Model):
    detail_name = models.CharField(unique=True, max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=6, blank=True, null=True)
    purpose = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.detail_name

class Color(models.Model):
    color_name = models.CharField(unique=True, max_length=50, blank=True, null=True)
    color_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    def __str__(self):
        return self.color_name

class Sale(models.Model):
    sale_name = models.CharField(unique=True, max_length=50, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    def __str__(self):
        return self.sale_name
class Fit(models.Model):
    fit_name = models.CharField(unique=True, max_length=50, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    def __str__(self):
        return self.fit_name
class Material(models.Model):
    material_name = models.CharField(unique=True, max_length=50, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    def __str__(self):
        return self.material_name

class Item(models.Model):
    item_name = models.CharField(max_length=50, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    on_sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True, default="default.jpg")
    details = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    fit = models.ForeignKey(Fit, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return self.item_name

class Review(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default='')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    


class CartItem(models.Model):
    itemInCart = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    cartOwner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default='')
    size = models.CharField(max_length=2, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    added = models.DateTimeField(auto_now_add=True)
    purchased = models.CharField(max_length=5, blank=True, null=True, default="False")
    def __str__(self):
        return str(self.cartOwner)+" "+str(self.itemInCart)

class Purchase(models.Model):
    purchasedItemIds = models.CharField(max_length=500, null=True, blank=True)
    purchaseOwner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default='')
    size = models.CharField(max_length=2, blank=True, null=True)
    totalPrice = models.CharField(max_length=400, null=True, blank=True)
    purchaseDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.purchaseOwner)+"; "+"$"+self.totalPrice+"; "+str(self.purchaseDate)
# @reciever(post_save, sender=User)
# def orderMade(sender, instance, created, **kwargs):
#     print("order made")
#     print('instance:', instance)
#     print('created:', created)

# post_save.connect(orderMade, sender=User)