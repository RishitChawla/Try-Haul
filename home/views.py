from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import Listing, Category, ProductType, Listing, Brand, User


# Create your views here.
def index(request):
    return render(request, "index.html")

def login(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")

def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/signup.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "signup.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "signup.html")

@login_required
def logout(request):
    try:
        logout(request)
        return HttpResponseRedirect(reverse("index"))
    except:
        return HttpResponseRedirect(reverse("index"))


def inventory(request):
    if request.user.is_staff:
        return render(request, "inventory.html")
    raise PermissionDenied

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

def bestSellers(request):
    listings = Listing.objects.filter(bestSelling=True)
    return render(request, "listing.html", {
        "listings": listings
    })

def newArrivals(request):
    listings = Listing.objects.filter(newArrival=True)
    return render(request, "listing.html", {
        "listings": listings
    })

def specialOffers(request):
    listings = Listing.objects.filter(specialOffer=True)
    return render(request, "listing.html", {
        "listings": listings
    })

def brand(request, brand_slug):
    brand = get_object_or_404(Brand, slug=brand_slug)
    listings = Listing.objects.filter(brand=brand)

    return render(request, "listing.html", {
        "listings": listings,  
    })

def brandlist(request):
    brands = Brand.objects.all()
    return render(request, "brandlist.html", {
        "brands": brands
    })

def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    listings = Listing.objects.filter(category=category)

    return render(request, "listing.html", {
        "listings": listings,
        "category": category.name,
    })

def productType(request, category_slug, productType_slug):
    category = get_object_or_404(Category, slug=category_slug)
    productType = get_object_or_404(ProductType, slug=productType_slug)
    listings = Listing.objects.filter(category=category, productType=productType)

    return render(request, "listing.html", {
        "listings": listings,
        "category": category.name,
        "productType": productType.name
    })

def item(request, category_slug, productType_slug, listing_slug):
    category = get_object_or_404(Category, slug=category_slug)
    productType = get_object_or_404(ProductType, slug=productType_slug)
    listing = get_object_or_404(Listing, category=category, productType=productType, slug=listing_slug)

    return render(request, "item.html", {
        "listing": listing
    })
