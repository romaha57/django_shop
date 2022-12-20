from django.contrib import admin

from .models import Basket, Product, ProductCategory


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    search_fields = ('name',)
    list_filter = ('category',)


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity')
    extra = 0


admin.site.register(ProductCategory)
admin.site.register(Product, ProductAdmin)
