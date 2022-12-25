from django.urls import path

from .views import (CancelOrderView, OrderCreateView, OrderDetailView,
                    OrdersListview, SuccessOrderView)

# namespace for order app
app_name = 'order'

urlpatterns = [
    path('', OrdersListview.as_view(), name='orders_list'),
    path('order/<int:pk>', OrderDetailView.as_view(), name='order'),
    path('order_create/', OrderCreateView.as_view(), name='order_create'),
    path('order-success/', SuccessOrderView.as_view(), name='order_success'),
    path('order-cancel/', CancelOrderView.as_view(), name='order_cancel'),
]
