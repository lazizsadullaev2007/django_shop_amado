from django.shortcuts import render, HttpResponse
from .models import Product, Category
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.

def home_view(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'store/index.html', context)

def shop_view(request):
    query = request.GET.get('search')
    if query:
        products = Product.objects.filter(Q(name__iregex=query))
    else:
        view = request.GET.get('view')
        sort_by = request.GET.get('sort_by')
        if sort_by:
            products = Product.objects.filter().order_by(sort_by)
        else:
            products = Product.objects.filter().order_by('-pk')
        if view:
            paginator = Paginator(products, view)
        else:
            paginator = Paginator(products, 1)
        page = request.GET.get('page')
        products = paginator.get_page(page)


    context = {
        'products': products
    }
    return render(request, 'store/shop.html', context)

def category_products_view(request, category_id):
    category = Category.objects.get(pk=category_id)
    view = request.GET.get('view')
    sort_by = request.GET.get('sort_by')
    if sort_by:
        products = Product.objects.filter(category=category).order_by(sort_by)
    else:
        products = Product.objects.filter(category=category).order_by('-pk')
    if view:
        paginator = Paginator(products, view)
    else:
        paginator = Paginator(products, 1)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    context = {
        'products': products
    }
    return render(request, 'store/shop.html', context)

def product_detail(request, slug ):
    product = Product.objects.filter(slug=slug).first()
    context = {
        'product': product
    }
    return render(request, 'store/product_detail.html', context)