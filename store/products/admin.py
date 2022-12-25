from django.contrib import admin

from .models import Basket, Product, ProductCategory


class ProductAdmin(admin.ModelAdmin):
    """Отображение в admin/ продуктов"""

    list_display = ('name', 'price', 'quantity', 'category', 'stripe_product_price_id')
    search_fields = ('name',)
    list_filter = ('category',)


class BasketAdmin(admin.TabularInline):
    """Отображение в admin/ корзины продуктов"""

    model = Basket
    fields = ('product', 'quantity')
    extra = 0


admin.site.register(ProductCategory)
admin.site.register(Product, ProductAdmin)
