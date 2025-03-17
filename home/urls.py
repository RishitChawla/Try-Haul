from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("orders", views.orders, name="orders"),
    path("edit", views.editProfile, name="editProfile"),
    path('wishlist', views.wishlist, name="wishlist"),
    path('cart', views.cart, name="cart"),
    path('allproducts', views.allProducts, name="allProducts"),
    path('<str:category>/', views.category, name="category"),
    # path('<str:category>/<str:productType>/<int:uniqueLabel>/', views.listing, name='listing'), # Item display
    path('<str:category>/<str:productType>', views.productType, name="productType"),

]
