from django.urls import path
from orders.views import OrderCreateView, SuccessTemplateView, yookassa_webhook_view



app_name = 'orders'



urlpatterns = [
    path('order-create', OrderCreateView.as_view(), name='order-create'),
    path('order-success', SuccessTemplateView.as_view(), name='order-success'),
    path('webhook/yookassa/', yookassa_webhook_view, name='yookassa_webhook'),
]











