from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages


from .models import Listing, Category, ProductType, Listing, Brand, User, Cart, Wishlist, Size


# Create your views here.
def index(request):
    return render(request, "index.html")

def login_view(request):
    if request.user.is_authenticated:
        return reverse("index")
    
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

def signup_view(request):
    if request.user.is_authenticated:
        return reverse("index")
    
    if request.method == "POST":
        firstName_ = request.POST["firstName"]
        lastName_ = request.POST["lastName"]
        email_ = request.POST["email"]
        phone_ = request.POST["phone"]
        

        # Ensure password matches confirmation
        password_ = request.POST["password"]
        confirmation_ = request.POST["confirmation"]
        if password_ != confirmation_:
            return render(request, "signup.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username=email_,
                firstName=firstName_,
                lastName=lastName_, 
                email=email_, 
                phone=phone_,
                password=password_)
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
def logout_view(request):
    try:
        logout(request)
        return HttpResponseRedirect(reverse("index"))
    except:
        return HttpResponseRedirect(reverse("index"))


def inventory(request):
    if request.user.is_staff:
        return render(request, "inventory.html")
    raise PermissionDenied


@login_required(login_url="/login")
def orders(request):
    return render(request, "orders.html")


@login_required(login_url="/login")
def editProfile(request):
    return render(request, "editProfile.html")


@login_required(login_url="/login")
def wishlist(request):
    user = request.user
    listings = Wishlist.objects.filter(wishlistUser=user)
    
    return render(request,"wishlist.html", {
        "listings": listings,
    })


@login_required(login_url="/login")
def cart(request):
    listings = Cart.objects.filter(cartUser=request.user)
    
    return render(request, "cart.html",{
        "listings": listings,
    })


def allProducts(request):
    listings = Listing.objects.all().order_by("-createdAt")
    return render(request, "listing.html", {
        'listings': listings,
        "category": "All Products"
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
    if category_slug in ["male", "female"]:
        listings = Listing.objects.filter(category__slug__in=[category_slug, "unisex"])
    else:
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

    is_in_wishlist = Wishlist.objects.filter(wishlistUser=request.user, wishlistItem=listing).exists()

    if request.method == "POST":
        
        if "addCart" in request.POST:   
            if not Cart.objects.filter(cartUser=request.user, cartItem=listing).exists(): # Add Is doesnt Exist
                
                selectedSize = request.POST.get("size")
                if not selectedSize:
                    messages.error(request, "Please select a size before adding to the cart.")
                    return redirect(request.META.get("HTTP_REFERER", "index"))

                sizeInstance = get_object_or_404(Size, size_label=selectedSize)

                Cart.objects.create(cartUser=request.user, cartItem=listing, cartSize=sizeInstance)
                messages.success(request, "Item added to cart!")  
            
            else: # Don't add if exists
                messages.info(request, "Item is already in the cart.")


        if "addWishlist" in request.POST:

            wishlist_item = Wishlist.objects.filter(wishlistUser=request.user, wishlistItem=listing)
            if wishlist_item.exists():
                wishlist_item.delete()  # Remove from wishlist
                is_in_wishlist = False
                messages.success(request, "Item removed from wishlist.")  
            else:
                Wishlist.objects.create(wishlistUser=request.user, wishlistItem=listing) # Add to the Wishlist
                messages.success(request, "Item added to wishlist!")  
                is_in_wishlist = True

            return redirect(reverse("item", args=[category_slug, productType_slug, listing_slug]))       
        
        if "addCartThroughWishlist" in request.POST:
            if not Cart.objects.filter(cartUser=request.user, cartItem=listing).exists():
                Cart.objects.create(cartUser=request.user, cartItem=listing)
                messages.success(request, "Item added to cart!")  
            else:
                messages.info(request, "Item is already in the cart.")

            return redirect(reverse("wishlist"))
        
        if "removeWishlistThroughWishlist" in request.POST:
            wishlist_item = Wishlist.objects.filter(wishlistUser=request.user, wishlistItem=listing)
            if wishlist_item.exists():
                wishlist_item.delete()  # Remove from wishlist
                is_in_wishlist = False
                messages.success(request, "Item removed from wishlist.")  
            else:
                Wishlist.objects.create(wishlistUser=request.user, wishlistItem=listing) # Add to the Wishlist
                messages.success(request, "Item added to wishlist!")  
                is_in_wishlist = True

            return redirect(reverse("wishlist"))

    return render(request, "item.html", {
        "listing": listing,
        "is_in_wishlist": is_in_wishlist,
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


def terms(request):
    return render(request, "terms.html")


def privacy(request):
    return render(request, "privacy.html")


def faq(request):
    return render(request, "FAQ.html")


def returnExchange(request):
    return render(request, "returnExchange.html")


def aboutUs(request):
    return render(request, "aboutUs.html")