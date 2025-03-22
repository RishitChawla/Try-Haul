from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    # Listings
    path('allproducts', views.allProducts, name="allProducts"),    
    path('bestsellers', views.bestSellers, name="bestSellers"),
    path('newarrivals', views.newArrivals, name="newArrivals"),
    path('specialoffers', views.specialOffers, name="specialOffers"),

    # Login     
    path("login", views.login_view, name="login"),
    path('signup', views.signup_view, name="signup"),
    path('logout', views.logout_view, name="logout"),


    path("inventory", views.inventory, name="inventory"),
    
    # After Login
    path("orders", views.orders, name="orders"),
    path("edit", views.editProfile, name="editProfile"),
    path('wishlist', views.wishlist, name="wishlist"),
    path('cart', views.cart, name="cart"),

    # Help
    path('terms-of-service', views.terms, name="termsOfServices"),
    path('privacy-policy', views.privacy, name="privacyPolicy"),
    path('FAQ', views.faq, name="FAQ"),
    path('return-exchange-policy', views.returnExchange, name="returnExchangePolicy"),
    path('about-us', views.aboutUs, name="aboutUs"),
    
    # Brandlist
    path('brandlist/', views.brandlist, name='brandlist'),
    
    # Categorise Brands 
    path('brandlist/<slug:brand_slug>/', views.brand, name="brand"),

    # Categorise gender, type and product
    path('<slug:category_slug>/', views.category, name="category"),
    path('<slug:category_slug>/<slug:productType_slug>/', views.productType, name="productType"),
    path('<slug:category_slug>/<slug:productType_slug>/<slug:listing_slug>/', views.item, name='item'),
]
