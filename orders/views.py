from django.forms import BaseModelForm
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from .forms import OrderForm
from common.views import titleMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import HttpResponseRedirect
import uuid
from store import settings
from yookassa import Configuration, Payment
from http import HTTPStatus
import json
from django.http import HttpResponse
from yookassa.domain.notification import WebhookNotification
from django.views.decorators.csrf import csrf_exempt

Configuration.account_id = 342769
Configuration.secret_key = 'test_Vb7ZZyumJs-2lCDn73a7B5lj02eJNycs5zNjxeN14hI'

class SuccessTemplateView(titleMixin, TemplateView):
    title = "Успешная оплата"
    template_name = 'orders/success.html'


class CanceledTemplateView(TemplateView):
    title = 'Ошибка при оплате'
    template_name = ''

class OrderCreateView(titleMixin, CreateView):
    title = "Store - оформление заказа"

    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order-create')

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)

        payment = Payment.create({
            "amount": {
                "value": "100.00",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "{}{}".format(settings.DOMAIN_NAME, reverse('orders:order-success'))
            },
            "capture": True,
            "description": "Заказ №1234"
        }, uuid.uuid4())
    
        return HttpResponseRedirect(payment.confirmation.confirmation_url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)

@csrf_exempt
def yookassa_webhook_view(request):
    # Проверяем, что запрос является POST запросом
    if request.method == 'POST':
        # Получаем тело запроса
        request_body = request.body.decode('utf-8')
        # Получаем заголовок с подписью
        signature_header = request.headers.get('Content-HMAC')
        # Создаем объект уведомления от Юкассы
        notification = WebhookNotification(request_body, signature_header)
        # Проверяем подпись уведомления
        if notification.check_signature():
            # Обрабатываем типы событий
            if notification.event == 'payment.succeeded':
                # Обработка успешной оплаты
                print("Успешная оплата:", notification.payload)
            elif notification.event == 'payment.canceled':
                # Обработка отмены оплаты
                print("Отмена оплаты:", notification.payload)
            # Возвращаем HTTP ответ с кодом 200, чтобы Юкасса поняла, что уведомление получено
            return HttpResponse(status=200)
        else:
            # Возвращаем HTTP ответ с кодом 403, если подпись не совпадает
            return HttpResponse(status=403)
    else:
        # Возвращаем HTTP ответ с кодом 405, если запрос не является POST запросом
        return HttpResponse(status=405)
