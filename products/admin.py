from django.contrib import admin

from products.models import Product, ProductsCategoty

admin.site.register(Product)
admin.site.register(ProductsCategoty)