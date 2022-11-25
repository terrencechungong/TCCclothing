from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.menCatalog, name="profiles"),
    path('projec/<id>/', views.project, name="project"),
    path('men/', views.menCatalog, name="men"),
    path('men/<type>/', views.menCatalogSpecific, name="men-specific"),
    path('women/<type>/', views.womenCatalogSpecific, name="women-specific"),
    path('kids/<type>/', views.kidsCatalogSpecific, name="kids-specific"),
    path('women/', views.womenCatalog, name="women"),
    path('sale/<gender>/', views.saleCatalog, name="sale"),
    path('kids/', views.kidsCatalog, name="kids"),
    path('register/', views.SignUp.as_view(), name="register"),
    path('login/', views.login_view, name='login'),
    path('cart/', views.cartView, name="cart"),
    path('logout/', views.logout_view, name="logout"),
    path('account/', views.userAccount, name="account"),
    path('account-details/', views.accountDetails, name="account-details"),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('edit-account/', views.editAccount, name="edit-account"),
    path('password_change_form/', auth_views.PasswordChangeView.as_view(), name="password_change_form"),
     path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
     path('addToCart/<item>/', views.addToCartView, name='addToCartView'),
     path('purchaseSuccess/' , views.purchaseView, name='purchaseSuccess'),
     path('updateCartItem/<pk>/', views.AddCartItem, name="updateCartItem"),
     path('deleteCartItem/<pk>/', views.DeleteCartItem, name="deleteCartItem")
]
