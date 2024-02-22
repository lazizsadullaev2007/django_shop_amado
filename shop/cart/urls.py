from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('cart/<int:product_id>/<str:action>/', views.to_cart, name='to_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('payment/', views.create_checkout_session, name='payment'),
    path('payment/success/', views.success_payment, name='success_payment')
]