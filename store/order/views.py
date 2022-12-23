from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from products.models import Basket
from utils.mixins import TitleMixin

from .forms import OrderCreateForm
from .models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


class SuccessOrderView(TitleMixin, TemplateView):
    template_name = 'order/success.html'
    title = 'Заказ успешно оплачен'


class CancelOrderView(TitleMixin, TemplateView):
    template_name = 'order/cancel.html'
    title = 'Ошибка при заказе'


class OrdersListview(TitleMixin, ListView):
    template_name = 'order/orders.html'
    context_object_name = 'orders'
    model = Order
    title = 'Заказы'
    ordering = ('-created_at',)


class OrderDetailView(DetailView):
    template_name = 'order/order.html'
    context_object_name = 'order'

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Заказ № {self.object.id}'

        return context


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'order/order-create.html'
    form_class = OrderCreateForm
    success_url = reverse_lazy('order:order_create')
    title = 'Оформление заказа'

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=request.user)

        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.get_stripe_price_id(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url=f'{settings.DOMAIN_NAME}{reverse_lazy("order:order_success")}',
            cancel_url=f'{settings.DOMAIN_NAME}{reverse_lazy("order:order_cancel")}',
        )
        return redirect(checkout_session.url, HTTPStatus.SEE_OTHER)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.request.user)

        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
          payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = stripe.checkout.Session.retrieve(
          event['data']['object']['id'],
          expand=['line_items'],
        )

        fulfill_order(session)

        return HttpResponse(status=200)


def fulfill_order(session):
    order_id = int(session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()
