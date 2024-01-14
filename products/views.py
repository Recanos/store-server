from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from products.models import Product, ProductsCategoty, Basket
from users.models import User
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    context = {'title' : 'Store!'}
    return render(request, 'products/index.html', context )

def products(request, category_id=None, page_number=1):
    if category_id:
        product = Product.objects.filter(category=category_id)
    else:
        product = Product.objects.all()

    paginator = Paginator(product, per_page=3)
    products_paginator = paginator.page(page_number)

    context = {'title' : 'Store - Каталог',
               'products' : products_paginator,
               'categories' : ProductsCategoty.objects.all() 
            }
    return render(request, 'products/products.html', context)

@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)
    if not baskets.exists():
        Basket.objects.create(user=request.user,product=product, quantity = 1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


