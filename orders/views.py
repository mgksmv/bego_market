from django.shortcuts import render, redirect
from django.contrib import messages
import datetime

from cart.models import CartItem
from .models import Order, OrderProduct
from .forms import OrderForm


def place_order(request, total=0, quantity=0):
    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('products')

    total = 0
    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.email = form.cleaned_data['email']
            data.phone = form.cleaned_data['phone']
            data.city = form.cleaned_data['city']
            data.street = form.cleaned_data['street']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = total
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            for cart_item in cart_items:
                orderproduct = OrderProduct()
                orderproduct.order = data
                orderproduct.user = data.user
                orderproduct.product = cart_item.product
                orderproduct.quantity = cart_item.quantity
                orderproduct.product_price = cart_item.product.price
                orderproduct.save()

            # Generate order number
            day = int(datetime.date.today().strftime('%d'))
            month = int(datetime.date.today().strftime('%m'))
            year = int(datetime.date.today().strftime('%Y'))
            date = datetime.date(year, month, day)
            current_date = date.strftime('%Y%m%d')

            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            messages.success(request, 'Заказ принят! Ожидайте звонка для уточнения деталей.')
            return redirect('my_orders')
    else:
        return redirect('checkout')


def orders(request):
    return render(request, 'orders/all_orders.html')


def order_complete(request):
    return render(request, 'orders/order_complete.html')
