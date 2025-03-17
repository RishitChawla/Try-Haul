from django.shortcuts import render, get_object_or_404
from .models import Listing, Category, ProductType
from django.http import HttpResponse
from .models import Listing

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

def allProducts(request):
    listings = Listing.objects.all().order_by("-createdAt")
    return render(request, "listing.html", {
        'listings': listings,
        "category": "All Products"
    })


def category(request, category):
    # Fetch listings that match the category name
    listings = Listing.objects.filter(category__name=category)

    return render(request, "listing.html", {
        "listings": listings,
        "category": category,
    })

def productType(request, category, productType):
    listings = Listing.objects.filter(category__name=category, productType__name=productType)

    return render(request, "listing.html", {
        "listings": listings,
        "category": category,
        "productType": productType
    })

def item(request, category, productType, uniqueLabel):
    return render(request, "item.html")
