from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("orders", views.orders, name="orders"),
    path("edit", views.editProfile, name="editProfile"),
    path('wishlist', views.wishlist, name="wishlist"),
    path('cart', views.cart, name="cart"),
    path('allproducts', views.allProducts, name="allProducts"),    
    path('bestsellers', views.bestSellers, name="bestSellers"),
    path('newarrivals', views.newArrivals, name="newArrivals"),
    path('specialoffers', views.specialOffers, name="specialOffers"),

    # Brandlist
    path('brandlist/', views.brandlist, name='brandlist'),
    
    # ✅ FIX: Brands now have a `/brand/` prefix
    path('brandlist/<slug:brand_slug>/', views.brand, name="brand"),

    # ✅ Categories remain without a prefix
    path('<slug:category_slug>/', views.category, name="category"),
    path('<slug:category_slug>/<slug:productType_slug>/', views.productType, name="productType"),
    path('<slug:category_slug>/<slug:productType_slug>/<slug:listing_slug>/', views.item, name='item'),
]
