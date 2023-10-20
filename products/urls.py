from django.urls import path

app_name = 'products'
from products.views import products
urlpatterns = [
    path('', products, name='index'),
]
