from django.shortcuts import render

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
