from app_users.models import CustomUser
from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=128, verbose_name='название категории')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=128, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    quantity = models.PositiveIntegerField(default=0, verbose_name='количество товара на складе')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='цена')
    image = models.ImageField(upload_to='image_for_products', verbose_name='фото товара')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='категория товара')

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ('name',)

    def __str__(self):
        return self.name


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum((basket.sum_products() for basket in self))

    def total_quantity(self):
        return sum((basket.quantity for basket in self))


class Basket(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='корзина для пользователя')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='товар')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='количество товара в корзине')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')

    objects = BasketQuerySet.as_manager()

    class Meta:
        verbose_name = 'корзина товара'
        verbose_name_plural = 'корзины товаров'

    def sum_products(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f'{self.user} ||| {self.product}'
