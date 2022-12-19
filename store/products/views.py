from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import ProductCategory, Product, Basket


def index(request):
    return render(request, 'products/index.html')


def show_catalog(request, category_id=None, page_number=1):
    products = Product.objects.all() if category_id is None else Product.objects.filter(category=category_id)
    paginator = Paginator(products, 3)
    products = paginator.page(page_number)
    categories = ProductCategory.objects.all()
    return render(request, 'products/catalog.html', {'products': products, 'categories': categories})


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
