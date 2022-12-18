from django.urls import path

from .views import index, show_catalog

app_name = 'products'

urlpatterns = [
    path('', index, name='index'),
    path('catalog/', show_catalog, name='catalog')
]