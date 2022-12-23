from app_users.models import CustomUser
from django.db import models
from products.models import Basket


class Order(models.Model):
    CREATED_ORDER = 1
    PAID = 2
    ON_WAY = 3
    COMPLETE = 4
    STATUS_CHOICES = (
        (CREATED_ORDER, 'создан'),
        (PAID, 'оплачен'),
        (ON_WAY, 'в пути'),
        (COMPLETE, 'выполнен'),
    )

    first_name = models.CharField(max_length=128, verbose_name='имя')
    last_name = models.CharField(max_length=128, verbose_name='фамилия')
    email = models.EmailField(verbose_name='email')
    address = models.CharField(max_length=255, verbose_name='адрес')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='покупатель')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    basket_history = models.JSONField(default=dict, verbose_name='история корзины')
    status = models.SmallIntegerField(default=CREATED_ORDER, choices=STATUS_CHOICES)

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'user:{self.user.username}, №{self.id}'

    def update_after_payment(self):
        baskets = Basket.objects.filter(user=self.user)
        self.status = self.PAID
        self.basket_history = {
            'products': [basket.history_in_json() for basket in baskets],
            'total_sum': float(baskets.total_sum())
        }
        baskets.delete()
        self.save()
