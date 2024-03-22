from django.urls import path

app_name = 'products'
from products.views import ProductsListView, basket_add, basket_remove

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),
    path('category/<int:category_id>', ProductsListView.as_view(), name='category'),
    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),
    path('baskets/delete/<int:basket_id>/', basket_remove, name='basket_remove'),
]