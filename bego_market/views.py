from django.shortcuts import render

from store.models import Product, Brand
from cart.models import Wishlist


def home(request):
    products = Product.objects.all().filter(is_available=True)
    brands = Brand.objects.all()

    wishlist_products = None

    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user)
        wishlist_products = [product.product.id for product in wishlist]

    context = {
        'products': products,
        'brands': brands,
        'wishlist_products': wishlist_products,
    }

    return render(request, 'main/home.html', context)


def about(request):
    return render(request, 'main/about.html')


def payment_and_delivery(request):
    return render(request, 'main/payment_and_delivery.html')


def laboratory(request):
    return render(request, 'main/laboratory.html')


def contact(request):
    return render(request, 'main/contact.html')
