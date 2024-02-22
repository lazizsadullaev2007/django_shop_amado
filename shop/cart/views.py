from django.shortcuts import render, HttpResponse, redirect
from .forms import CustomerForm
from .utils import CartForAnonymousUser, CartForAuthenticatedUser, get_cart_data
import stripe
from shop import settings
from django.urls import reverse

# Create your views here.


def home_view(request):
    cart_info = get_cart_data(request)
    context = {
        'cart_total_quantity': cart_info['cart_total_quantity'],
        'cart_total_price': cart_info['cart_total_price'],
        'products': cart_info['products'],
        'order': cart_info['order']
    }
    return render(request, 'cart/cart.html', context)


def to_cart(request, product_id, action):
    if request.user.is_authenticated:
        user_cart = CartForAuthenticatedUser(request, product_id, action)
    else:
        session_cart = CartForAnonymousUser(request, product_id, action)

    return redirect('cart:home')

def checkout_view(request):
    cart_data = get_cart_data(request)

    if request.method == "POST":
        form = CustomerForm(data=request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CustomerForm()

    context = {
        'form': form,
        'total_price': cart_data['cart_total_price']
    }

    return render(request, 'cart/checkout.html', context)

def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    if not request.user.is_authenticated:
        user_cart = CartForAnonymousUser(request)
    else:
        user_cart = CartForAuthenticatedUser(request)

    cart_info = user_cart.get_cart_info()
    total_price = cart_info['cart_total_price']

    session = stripe.checkout.Session.create(
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Products from Boutique web_site',
                    },
                    'unit_amount': int(total_price * 100)
                },
                'quantity': 1
            }
        ],
        mode='payment',
        success_url = request.build_absolute_uri(reverse('cart:success_payment')),
        cancel_url = request.build_absolute_uri(reverse('cart:success_payment'))
    )

    return redirect(session.url, 303)

def success_payment(request):
    if request.user.is_authenticated:
        user_cart = CartForAuthenticatedUser(request)
    else:
        user_cart = CartForAnonymousUser(request)
    user_cart.clear()
    return redirect('cart:home')

