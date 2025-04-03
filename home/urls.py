from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    # Listings
    path('all-products', views.allProducts, name="allProducts"),    
    path('best-sellers', views.bestSellers, name="bestSellers"),
    path('new-arrivals', views.newArrivals, name="newArrivals"),
    path('special-offers', views.specialOffers, name="specialOffers"),
    path('limited-drops', views.limitedDrops, name="limitedDrops"),
    

    # Login     
    path("login", views.login_view, name="login"),
    path('signup', views.signup_view, name="signup"),
    path('logout', views.logout_view, name="logout"),


    path("inventory", views.inventory, name="inventory"),
    path("search/", views.search_results, name="search_results"),
    
    # After Login
    path('wishlist', views.wishlist, name="wishlist"),
    path('cart', views.cart, name="cart"),
    path("apply-coupon/", views.apply_coupon, name="apply_coupon"),
    path("store-order/<str:totalAmount>/<str:totalMRP>/<str:discount>/<str:couponDiscount>/", views.storeOrderDetails, name="storeOrderDetails"),
    path("address/", views.address, name="address"),
    path('payment', views.payment, name="payment"),
    path("orders", views.orders, name="orders"),
    

    # path("edit", views.editProfile, name="editProfile"),
    
    path("pay/", views.initiatePayment, name="initiatePayment"),
    path("payment-success/", views.payment_success, name="payment_success"),
    path("payment-webhook/", views.payment_webhook, name="payment_webhook"),

    path("initiate/", views.initiate, name="initiate"),



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
