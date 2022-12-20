from products.models import ProductCategory


def categories(request):
    return {'categories': ProductCategory.objects.all()}
