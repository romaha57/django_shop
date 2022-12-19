from django.urls import path

from .views import index, show_catalog, add_in_basket, remove_from_basket

app_name = 'products'

urlpatterns = [
    path('', index, name='index'),
    path('catalog/', show_catalog, name='catalog'),
    path('page/<int:page_number>/', show_catalog, name='paginator'),
    path('category/<int:category_id>', show_catalog, name='category'),
    path('basket/add/<int:product_id>', add_in_basket, name='add_in_basket'),
    path('basket/remove/<int:basket_id>', remove_from_basket, name='remove_from_basket'),
]