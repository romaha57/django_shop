from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView

from utils.mixins import TitleMixin
from .models import Basket, Product


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Онлайн-магазин'


class ProductListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/catalog.html'
    context_object_name = 'products'
    paginate_by = 3
    title = 'Каталог товаров'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset if category_id is None else queryset.filter(category=category_id)


@login_required
def add_in_basket(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(
            user=request.user,
            product=product,
            quantity=1
        )

    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return redirect(request.META['HTTP_REFERER'])


@login_required
def remove_from_basket(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return redirect(request.META['HTTP_REFERER'])
