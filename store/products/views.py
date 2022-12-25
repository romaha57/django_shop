from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView

from utils.mixins import TitleMixin

from .models import Basket, Product


class IndexView(TitleMixin, TemplateView):
    """Отображение главной страницы"""

    template_name = 'products/index.html'
    title = 'Онлайн-магазин'


class ProductListView(TitleMixin, ListView):
    """Отображение каталога товаров и пагинация"""

    model = Product
    template_name = 'products/catalog.html'
    context_object_name = 'products'
    paginate_by = 3
    title = 'Каталог товаров'

    def get_queryset(self):
        """Фильтрует queryset по категории"""

        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset if category_id is None else queryset.filter(category=category_id)


@login_required
def add_in_basket(request, product_id):
    """Добавление в корзину товара"""

    Basket.create_or_update(product_id, request.user)

    return redirect(request.META['HTTP_REFERER'])


@login_required
def remove_from_basket(request, basket_id):
    """Удаление товара из корзины"""

    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return redirect(request.META['HTTP_REFERER'])
