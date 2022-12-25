from products.models import ProductCategory


def categories(request):
    """Контекст-процессор для отображения категории товаров"""

    return {'categories': ProductCategory.objects.all()}
