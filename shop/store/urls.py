from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('shop/', views.shop_view, name='shop'),
    path('shop/category/<str:category_id>/', views.category_products_view, name='category_products'),
    path('product/shop/<slug:slug>/', views.product_detail, name='detail')
]
