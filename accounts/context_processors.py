from store.models import Product
from cart.models import Wishlist


def wishlist_counter(request):
    if request.user.is_authenticated:
        products = Wishlist.objects.filter(user=request.user)
        wishlist_count = len(products)
    else:
        wishlist_count = 0

    return dict(wishlist_count=wishlist_count)

    # if 'admin' in request.path:
    #     return {}
    # else:
    #     try:
    #         cart = Cart.objects.filter(cart_id=_cart_id(request))
    #         if request.user.is_authenticated:
    #             cart_items = CartItem.objects.all().filter(user=request.user)
    #         else:
    #             cart_items = CartItem.objects.all().filter(cart=cart[:1])
    #         for cart_item in cart_items:
    #             cart_count += cart_item.quantity
    #     except Cart.DoesNotExist:
    #         cart_count = 0
