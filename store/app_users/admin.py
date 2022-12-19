from django.contrib import admin

from .models import CustomUser
from products.admin import BasketAdmin


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    inlines = (BasketAdmin, )


admin.site.register(CustomUser, CustomUserAdmin)