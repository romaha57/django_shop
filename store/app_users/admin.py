from django.contrib import admin

from .models import CustomUser, VerifyEmailModel
from products.admin import BasketAdmin


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    inlines = (BasketAdmin, )


class VerifyEmailModelAdmin(admin.ModelAdmin):
    list_display = ('unique_code', 'experation_link', 'user')
    readonly_fields = ('created_at',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(VerifyEmailModel, VerifyEmailModelAdmin)
