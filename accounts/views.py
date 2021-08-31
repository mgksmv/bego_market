from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.core import serializers
import requests

# Email verification imports
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# App imports
from store.models import Product
from .forms import RegistrationForm, UserForm
from .models import Account
from cart.models import Cart, CartItem, Wishlist
from cart.views import _cart_id
from orders.models import Order, OrderProduct


def account_activation(request, user, email):
    current_site = get_current_site(request)
    mail_subject = 'Активация аккаунта BEGO Market'
    message = render_to_string('accounts/account_verification_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })

    to_email = email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()


def resend_activation_link(request, email):
    user = Account.objects.get(email=email)
    email = email
    account_activation(request, user, email)
    return redirect(f'/account/login/?command=verification&email={email}')


def register(request):
    User = get_user_model()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        email = request.POST['email']

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email
            # username = email.split('@')[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email,
                                               username=username, password=password)
            user.phone_number = phone_number
            user.save()

            # User activation
            account_activation(request, user=user, email=email)
            return redirect(f'/account/login/?command=verification&email={email}')
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }

    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if cart_item_exists:
                    if not len(CartItem.objects.filter(user=user)) >= 1:
                        cart_items = CartItem.objects.filter(cart=cart)
                        for item in cart_items:
                            item.user = user
                            item.save()
            except:
                pass

            auth.login(request, user)
            messages.success(request, 'Вы успешно вошли.')

            # TODO 3: Redirect the user to Checkout from the Registration page too
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    next_page = params['next']
                    return redirect(next_page)
                return redirect('home')
            except:
                return redirect('dashboard')
        else:
            try:
                current_user = Account.objects.get(email=email)
                current_user_check_password = current_user.check_password(password)
                if Account.objects.filter(email=email,
                                          is_active=False).exists() and current_user_check_password is True:
                    return redirect(f'/account/login/?command=verification&email={email}')
            except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
                messages.error(request, 'Аккаунт с таким E-mail не существует.')
                return redirect('login')
            else:
                messages.error(request, f'E-mail или пароль неверны.')
                return redirect('login')

    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Вы вышли из аккаунта.')
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Ваш аккаунт активирован. Теперь Вы можете войти.')
        return redirect('login')
    else:
        messages.error(request, 'Недействительная ссылка.')
        return redirect('register')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password
            current_site = get_current_site(request)
            mail_subject = 'Сброс пароля'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            account_activation(request, user=user, email=email)

            messages.success(request, 'На Ваш E-mail адрес было отпралено письмо со ссылкой для сброса пароля.')
            return redirect('login')
        else:
            messages.error(request, 'Аккаунт с таким E-mail не существует.')
            return redirect('forgot_password')

    return render(request, 'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Пожалуйста, сбросьте свой пароль.')
        return redirect('reset_password')
    else:
        messages.error(request, 'Эта ссылка больше недействительна.')
        return redirect('login')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password and len(password) < 6:
            messages.error(request, 'Пароль должен состоять как минимум из 6 символов!')
            return redirect('reset_password')
        elif password == confirm_password and len(password) >= 6:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Пароль сброшен.')
            return redirect('login')
        else:
            messages.error(request, 'Пароли не совпадают!')
            return redirect('reset_password')
    else:
        return render(request, 'accounts/reset_password.html')


@login_required(login_url='login')
def dashboard(request):
    orders = Order.objects.filter(user_id=request.user.id).order_by('-created_at')
    orders_count = orders.count()

    context = {
        'orders_count': orders_count,
    }

    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'orders': orders,
    }

    return render(request, 'accounts/my_orders.html', context)


@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Ваш профиль обновлён.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)

    context = {
        'user_form': user_form,
    }

    return render(request, 'accounts/edit_profile.html', context)


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password and new_password != current_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Пароль изменён.')
                return redirect('change_password')
            else:
                messages.error(request, 'Текущий пароль неверный! Пожалуйста, введите правильный пароль.')
                return redirect('change_password')
        elif new_password == confirm_password and new_password == current_password:
            messages.error(request, 'Новый пароль не может быть старым паролем!')
            return redirect('change_password')
        else:
            messages.error(request, 'Пароли не совпадают!')
            return redirect('change_password')

    return render(request, 'accounts/change_password.html')


@login_required(login_url='login')
def order_details(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)

    context = {
        'order_detail': order_detail,
        'order': order,
    }

    return render(request, 'accounts/order_detail.html', context)


@login_required(login_url='login')
def wishlist(request):
    if request.user.is_authenticated:
        wishlist = None
        wishlist_products = None
        products = Wishlist.objects.filter(user=request.user)

        if request.user.is_authenticated:
            wishlist = Wishlist.objects.filter(user=request.user)
            wishlist_products = [product.product.id for product in wishlist]

        context = {
            'products': products,
            'wishlist_products': wishlist_products,
        }

        return render(request, 'accounts/wishlist.html', context)


@login_required(login_url='login')
def add_to_wishlist(request):
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
