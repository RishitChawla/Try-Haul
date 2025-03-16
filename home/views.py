from django.shortcuts import render, get_object_or_404
from .models import Listing, Category, ProductType

# Create your views here.
def index(request):
    return render(request, "index.html")

def orders(request):
    return render(request, "orders.html")

def editProfile(request):
    return render(request, "editProfile.html")

def wishlist(request):
    return render(request,"wishlist.html")

def cart(request):
    return render(request, "cart.html")

def listing(request, category, productType, uniqueLabel):
    categoryObj = get_object_or_404(Category, name=category)
    productTypeObj = get_object_or_404(ProductType, name=productType)
    
    product = get_object_or_404(
        Listing,
        category=categoryObj,
        productType=productTypeObj,
        uniqueLabel=uniqueLabel
    )

    return render(request, 'listing.html', {
        'product': product
        })
