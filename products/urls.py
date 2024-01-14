from django.urls import path

app_name = 'products'
from products.views import products, basket_add, basket_remove
urlpatterns = [
    path('', products, name='index'),
    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),
    path('baskets/delete/<int:basket_id>/', basket_remove, name='basket_remove'),
]
