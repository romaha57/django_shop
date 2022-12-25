from django.contrib import admin

from .models import Order


class OrderAdmin(admin.ModelAdmin):
    """Отображение в admin/ заказов"""

    list_display = ('__str__', 'status')
    readonly_fields = ('created_at',)
    list_filter = ('status',)


admin.site.register(Order, OrderAdmin)
