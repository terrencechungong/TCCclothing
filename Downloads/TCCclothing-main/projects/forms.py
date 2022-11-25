from cProfile import Profile
from .models import Review, CartItem, Purchase
from  django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView, CreateView
from django.views import generic


class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','phone_number','password1','password2','gender']

class CustomUserUpdateForm(UpdateView):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','phone_number']

# create update form for users
class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','phone_number']

class CommentForm(ModelForm):
    class Meta:
        model = Review
        fields = ['body']

class CartAddForm(ModelForm):
    class Meta:
        model = CartItem
        fields = '__all__'

class PurchaseForm(ModelForm):
    class Meta:
        model = Purchase
        fields = '__all__'