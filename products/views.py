from typing import Any

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.shortcuts import HttpResponseRedirect, render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import titleMixin
from products.models import Basket, Product, ProductsCategoty
from users.models import User


# Create your views here.
class IndexView(titleMixin, TemplateView):
    template_name = 'products/index.html'
    title = "Welcome!!!"



class ProductsListView(titleMixin, ListView):
    model = Product
    paginate_by = 3
    template_name = 'products/products.html'
    title = "Store - каталог"
    
    def get_queryset(self):
        querySet = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return querySet.filter(category_id=category_id) if category_id else querySet
    
    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        context['categories'] = ProductsCategoty.objects.all() 
        return context
        


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

