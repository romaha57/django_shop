import stripe
from app_users.models import CustomUser
from django.conf import settings
from django.db import models

stripe.api_key = settings.STRIPE_SECRET_KEY


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
    stripe_product_price_id = models.CharField(max_length=128, verbose_name='price id для stripe',
                                               null=True, blank=True)
    image = models.ImageField(upload_to='image_for_products', verbose_name='фото товара')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='категория товара')

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.stripe_product_price_id:
            stripe_price = self.get_stripe_price()
            self.stripe_product_price_id = stripe_price['id']
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    def get_stripe_price(self):
        print('ok')
        stripe_product = stripe.Product.create(name=self.name)
        stripe_price = stripe.Price.create(
            product=stripe_product['id'], unit_amount=round(self.price * 100), currency="rub"
        )
        return stripe_price


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum((basket.sum_products() for basket in self))

    def total_quantity(self):
        return sum((basket.quantity for basket in self))

    def get_stripe_price_id(self):
        line_items = []
        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity
            }
            line_items.append(item)

        return line_items


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

    def history_in_json(self):
        history_json = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'total_price': float(self.sum_products())
        }
        return history_json

    def __str__(self):
        return f'{self.user} ||| {self.product}'
