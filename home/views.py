from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.db.models import Q



from .models import Listing, Category, ProductType, Listing, Brand, User, Cart, Wishlist, Size, Stock, UserAddress, Coupon, SizeGuide


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

def apply_coupon(request):
    if request.method == "POST":
        coupon_code = request.POST.get("coupon_code")
        total_amount = float(request.POST.get("total_amount", 0))

        try:
            coupon = Coupon.objects.get(code=coupon_code, isActive=True)
            if total_amount >= coupon.minCartValue:
                discount_amount = (total_amount * coupon.percentage) / 100
                discount_amount = min(discount_amount, coupon.maxDiscount)

                return JsonResponse({
                    "success": True,
                    "discount": discount_amount,
                    "message": f"Coupon {coupon.code} applied successfully!",
                })
            else:
                return JsonResponse({
                    "success": False,
                    "message": f"Minimum order value must be ₹{coupon.minCartValue} to use this coupon."
                })
        except Coupon.DoesNotExist:
            return JsonResponse({"success": False, "message": "Invalid or expired coupon code."})
    
    return JsonResponse({"success": False, "message": "Invalid request."})




def storeOrderDetails(request, totalAmount, totalMRP, discount, couponDiscount):
    if request.method == "POST":
        if "saveAddressBtn" in request.POST:
            fullName = request.POST.get("full-name")
            phone = request.POST.get("phone")
            address = request.POST.get("address")
            city = request.POST.get("city")
            state = request.POST.get("state")
            pincode = request.POST.get("pincode")

            address = UserAddress(
                user=request.user,
                fullName=fullName,
                phone=phone,
                address=address,
                city=city,
                state=state,
                pincode=pincode
            )
            address.save()
        
        if "addAddressBtn" in request.POST:
            fullName = request.POST.get("full-name")
            phone = request.POST.get("phone")
            address = request.POST.get("address")
            city = request.POST.get("city")
            state = request.POST.get("state")
            pincode = request.POST.get("pincode")

            address = UserAddress(
                user=request.user,
                fullName=fullName,
                phone=phone,
                address=address,
                city=city,
                state=state,
                pincode=pincode
            )
            address.save()


        if "removeAddress" in request.POST:
            addressID = request.POST.get("addressID")
            
            address = get_object_or_404(UserAddress, id=addressID)
            address.delete()


        # Takes to payment page
        if "continueToPaymentBtn" in request.POST: 
            orderAddress = request.POST.get("selectedAddress")
            orderAddressObj = get_object_or_404(UserAddress, id=orderAddress)

            # Convert the object into a dictionary (store only essential fields)
            orderAddressData = {
                "fullName": orderAddressObj.fullName,
                "phone": orderAddressObj.phone,
                "address": orderAddressObj.address,
                "city": orderAddressObj.city,
                "state": orderAddressObj.state,
                "pincode": orderAddressObj.pincode,
            }

            request.session["payment_details"] = {
                "paymentAddress": orderAddressData,
                "paymentAmount": totalAmount
            }
            return redirect(reverse('payment'))


        # Redirect back to address page
        request.session['order_details'] = {
        'totalAmount': totalAmount,
        'totalMRP': totalMRP,
        'discount': discount,
        'couponDiscount': couponDiscount,
        }
        return redirect(reverse('address'))


    request.session['order_details'] = {
        'totalAmount': totalAmount,
        'totalMRP': totalMRP,
        'discount': discount,
        'couponDiscount': couponDiscount,
    }
    return redirect(reverse('address'))




def address(request):
    if 'order_details' not in request.session:
        return HttpResponseForbidden("Access Denied. Please proceed through the checkout.")


    order_details = request.session.get('order_details')  # Remove after use
    addresses = UserAddress.objects.filter(user=request.user)
    return render(request, 'userAddress.html', {
        "order_details":order_details,
        "addresses": addresses
    })


def payment(request):
    if 'payment_details' not in request.session:
        return HttpResponseForbidden("Access Denied. Please proceed through the checkout.")

    payment_details = request.session.pop('payment_details')
    return render(request, 'payment.html', payment_details)



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

    size_guide = SizeGuide.objects.filter(brand=listing.brand, category=listing.category, ProductType=listing.productType)

    if request.user.is_authenticated:
        is_in_wishlist = Wishlist.objects.filter(wishlistUser=request.user, wishlistItem=listing).exists()
    else:
        is_in_wishlist = False

    if request.method == "POST":
        
        # Add Item or increase quanity of cart from listing page
        if "addCart" in request.POST:   
            selectedSize = request.POST.get("size")
            
            if not selectedSize:
                messages.error(request, "Please select a size before adding to the cart.")
                return redirect(request.META.get("HTTP_REFERER", "index"))

            sizeInstance = get_object_or_404(Size, size_label=selectedSize)

            # Get stock for the selected size
            stock_item = Stock.objects.filter(listing=listing, size=sizeInstance).first()

            if not stock_item or stock_item.quantity <= 0:
                messages.error(request, "This size is out of stock!")
                return redirect(request.META.get("HTTP_REFERER", "index"))

            # Check if the item with the same size already exists in the cart
            cart_item, created = Cart.objects.get_or_create(
                cartUser=request.user, 
                cartItem=listing, 
                cartSize=sizeInstance,
            )

            if not created:  # If the item already exists, increase quantity
                if cart_item.cartQuantity + 1 > stock_item.quantity:
                    messages.error(request, "Not enough stock available!")
                else:
                    cart_item.cartQuantity += 1
                    cart_item.save()
                    messages.info(request, "Increased quantity in cart.")
            else:
                messages.success(request, "Item added to cart!")

        # Add to wishlist through item page
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
        
        # Remove from Wishlist from wishlist page
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
        
        if "removeCartItemFromCart" in request.POST:
            selectedSize = request.POST.get("size")
            sizeInstance = get_object_or_404(Size, size_label=selectedSize)
            
            item = Cart.objects.filter(cartUser=request.user, cartItem=listing, cartSize=sizeInstance)
            item.delete()
            return redirect(reverse("cart"))
        
        # Decrease the quantity of an item in cart
        if "decreaseQuantity" in request.POST:
            selectedSize = request.POST.get("size")
            sizeInstance = get_object_or_404(Size, size_label=selectedSize)

            # Get the object
            cart_item = get_object_or_404(
                Cart,
                cartUser=request.user, 
                cartSize=sizeInstance,
            )

            if cart_item.cartQuantity == 1:
                cart_item.delete()
                request.session["cart_message"] = {
                    "message": f"Removed {cart_item.cartItem.name} from cart.",
                    "cart_item_id": cart_item.id
                }
            else:
                cart_item.cartQuantity -= 1  # Decrease Quantity
                cart_item.save()
                request.session["cart_message"] = {
                    "message": f"Decreased quantity for {cart_item.cartItem.name}.",
                    "cart_item_id": cart_item.id
                }

            return redirect(reverse("cart"))

        # Increase the quantity of an item in the cart
        if "increaseQuantity" in request.POST:
            selectedSize = request.POST.get("size")
            sizeInstance = get_object_or_404(Size, size_label=selectedSize)

            # Get the object
            cart_item = get_object_or_404(
                Cart,
                cartUser=request.user, 
                cartSize=sizeInstance,
            )

            stock_item = Stock.objects.filter(listing=cart_item.cartItem, size=sizeInstance).first()

            if not stock_item or stock_item.quantity <= 0:
                request.session["cart_message"] = {
                    "message": "This size is out of stock!",
                    "cart_item_id": cart_item.id
                }
                return redirect(request.META.get("HTTP_REFERER", "index"))

            if cart_item.cartQuantity + 1 > stock_item.quantity:
                request.session["cart_message"] = {
                    "message": "Not enough stock available!",
                    "cart_item_id": cart_item.id
                }
            else:
                cart_item.cartQuantity += 1
                cart_item.save()
                request.session["cart_message"] = {
                    "message": f"Increased quantity for {cart_item.cartItem.name}.",
                    "cart_item_id": cart_item.id
                }

            return redirect(reverse("cart"))


    return render(request, "item.html", {
        "listing": listing,
        "is_in_wishlist": is_in_wishlist,
        "size_guide": size_guide
    })

# Clears the session message after displaying it
def clear_cart_message(request):
    request.session.pop("cart_message", None)
    return JsonResponse({"success": True})


def search_results(request):
    if request.method == "POST":
        query = request.POST.get("q")
        results = []

        if query:
            results = Listing.objects.filter(
            Q(name__icontains=query) |  # Search in listing names
            Q(brand__name__icontains=query)  # Search in brand names
        ).distinct()

        return render(request, "listing.html", {"query": query, "listings": results})


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

def limitedTimeDeals(request):
    listings = Listing.objects.filter(limitedTime=True)
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