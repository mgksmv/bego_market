from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q, Min, Max
import requests

from .models import Product, Brand
from category.models import Category
from cart.models import CartItem, Wishlist
from cart.views import _cart_id


def product_filter(request):
    product_id = request.GET['product']
    product = Product.objects.get(pk=product_id)

    wishlist_product = Wishlist.objects.filter(user=request.user, product=product)

    if wishlist_product.exists():
        wishlist_product.delete()
        data = {
            'bool': False,
        }
    else:
        wishlist_product = Wishlist.objects.create(user=request.user, product=product)
        data = {
            'bool': True,
        }

    return JsonResponse(data)


def products(request, category_slug=None):
    categories = None
    all_products = None
    paged_products = None
    wishlist = None
    wishlist_products = None

    brands = Brand.objects.all()
    min_max_price = Product.objects.aggregate(Min('price'), Max('price'))

    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user)
        wishlist_products = [product.product.id for product in wishlist]

    if category_slug != None:
        brand_list = None
        min_price = None
        max_price = None
        categories = get_object_or_404(Category, slug=category_slug)
        all_products = Product.objects.filter(category=categories, is_available=True).order_by('-id')

        if request.method == 'GET':
            try:
                brand_list = request.GET.getlist('brand')
                min_price = request.GET.getlist('minPrice')[0]
                max_price = request.GET.getlist('maxPrice')[0]

                if len(brand_list) == 0:
                    all_products = Product.objects.filter(category=categories, is_available=True, price__gte=min_price,
                                                          price__lte=max_price)
                else:
                    all_products = Product.objects.filter(category=categories, is_available=True, brand__in=brand_list,
                                                          price__gte=min_price, price__lte=max_price)
            except:
                pass

        ordering = request.GET.get('ordering', '')
        if ordering and ordering != 'all_products':
            all_products = all_products.order_by(ordering)
        else:
            pass

    else:
        brand_list = None
        min_price = None
        max_price = None
        all_products = Product.objects.all().filter(is_available=True).order_by('-id')

        if request.method == 'GET':
            try:
                brand_list = request.GET.getlist('brand')
                min_price = request.GET.getlist('minPrice')[0]
                max_price = request.GET.getlist('maxPrice')[0]
                if len(brand_list) == 0:
                    all_products = Product.objects.all().filter(is_available=True, price__gte=min_price,
                                                                price__lte=max_price).order_by('-id')
                else:
                    all_products = Product.objects.all().filter(is_available=True, brand__in=brand_list,
                                                                price__gte=min_price,
                                                                price__lte=max_price).order_by('-id')
            except:
                pass

        ordering = request.GET.get('ordering', '')
        if ordering and ordering != 'all_products':
            all_products = all_products.order_by(ordering)
        else:
            pass

    brand_list_int = []
    for brand in range(0, len(brand_list)):
        brand_id_int = int(brand_list[brand])
        brand_list_int.append(brand_id_int)

    paginator = Paginator(all_products, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = all_products.all().count()

    context = {
        'products': paged_products,
        'product_count': product_count,
        'brands': brands,
        'min_max_price': min_max_price,
        'wishlist': wishlist,
        'wishlist_products': wishlist_products,
        'brand_list_int': brand_list_int,
    }

    return render(request, 'store/products.html', context)


def product_detail(request, product_slug):
    single_product = Product.objects.get(slug=product_slug)
    wishlist_products = None
    if request.user.is_authenticated:
        in_cart = CartItem.objects.filter(user=request.user, product=single_product).exists()
        wishlist = Wishlist.objects.filter(user=request.user)
        wishlist_products = [product.product.id for product in wishlist]
    else:
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'wishlist_products': wishlist_products,
    }

    return render(request, 'store/product_detail.html', context)


def search(request):
    products = None
    product_count = 0

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }

    return render(request, 'store/products.html', context)


# Ajax filter
# def filter_data(request):
#     categories = request.GET.getlist('category[]')
#     brands = request.GET.getlist('brand[]')
#     min_price = request.GET['minPrice']
#     max_price = request.GET['maxPrice']
#
#     all_products = None
#
#     if 'category' in request.path:
#         last_url_element = request.path.split('/')[:-1]
#         all_products = Product.objects.all().filter(is_available=True, category__id__in=last_url_element).order_by('-id').distinct()
#     else:
#         all_products = Product.objects.all().filter(is_available=True).order_by('-id').distinct()
#
#     all_products = all_products.filter(price__gte=min_price)
#     all_products = all_products.filter(price__lte=max_price)
#
#     if len(categories) > 0:
#         all_products = all_products.filter(category__id__in=categories).distinct()
#     if len(brands) > 0:
#         all_products = all_products.filter(brand__id__in=brands).distinct()
#
#     data = render_to_string('ajax/product_list.html', {'products': all_products})
#     return JsonResponse({'products': data})


def brands(request):
    all_brands = Brand.objects.all()

    context = {
        'brands': all_brands,
    }

    return render(request, 'store/brands.html', context)


def brand_detail(request, brand_slug):
    brand = Brand.objects.get(slug=brand_slug)
    brand_products = Product.objects.filter(brand=brand)
    wishlist_products = None
    category_list = None

    min_max_price = brand_products.aggregate(Min('price'), Max('price'))

    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user)
        wishlist_products = [product.product.id for product in wishlist]

    category_ids = [brand_item.category.id for brand_item in brand_products]

    if request.method == 'GET':
        try:
            category_list = request.GET.getlist('category')
            min_price = request.GET.getlist('minPrice')[0]
            max_price = request.GET.getlist('maxPrice')[0]
            if len(category_list) == 0:
                brand_products = Product.objects.filter(brand=brand, price__gte=min_price, price__lte=max_price)
            else:
                brand_products = Product.objects.filter(brand=brand, category__id__in=category_list,
                                                        price__gte=min_price,
                                                        price__lte=max_price)
        except:
            pass

    category_list_int = []
    for category in range(0, len(category_list)):
        category_id_int = int(category_list[category])
        category_list_int.append(category_id_int)

    product_count = brand_products.all().count()

    context = {
        'brand': brand,
        'products': brand_products,
        'category_ids': category_ids,
        'min_max_price': min_max_price,
        'wishlist_products': wishlist_products,
        'product_count': product_count,
        'category_list_int': category_list_int,
    }

    return render(request, 'store/brand_detail.html', context)
