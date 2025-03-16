from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("orders", views.orders, name="orders"),
    path("edit", views.editProfile, name="editProfile"),
    path('wishlist', views.wishlist, name="wishlist"),
    path('cart', views.cart, name="cart")
]
