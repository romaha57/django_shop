from django.urls import path

from .views import (IndexView, ProductListView, add_in_basket,
                    remove_from_basket)

app_name = 'products'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('catalog/', ProductListView.as_view(), name='catalog'),
    path('page/<int:page>/', ProductListView.as_view(), name='paginator'),
    path('category/<int:category_id>', ProductListView.as_view(), name='category'),
    path('basket/add/<int:product_id>', add_in_basket, name='add_in_basket'),
    path('basket/remove/<int:basket_id>', remove_from_basket, name='remove_from_basket'),
]
