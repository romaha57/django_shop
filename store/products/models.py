import stripe
from django.conf import settings
from django.db import models

from app_users.models import CustomUser

# ключ для подключения платежной системы stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductCategory(models.Model):
    """Модель категории товаров"""

    name = models.CharField(max_length=128, verbose_name='название категории')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель товаров"""

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
        """При сохранении формы добавляем в поле у товара его stripe_product_price_id """

        if not self.stripe_product_price_id:
            stripe_price = self.get_stripe_price()
            self.stripe_product_price_id = stripe_price['id']
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    def get_stripe_price(self):
        """Функция для получения stripe_price, чтобы потом получить stripe_product_price_id"""

        stripe_product = stripe.Product.create(name=self.name)
        stripe_price = stripe.Price.create(
            product=stripe_product['id'], unit_amount=round(self.price * 100), currency="rub"
        )
        return stripe_price


class BasketQuerySet(models.QuerySet):
    """Класс для обращения к общим методам всех корзин товаров"""

    def total_sum(self):
        """Возвращает общую стомость всех товаров в корзине пользователя"""

        return sum((basket.sum_products() for basket in self))

    def total_quantity(self):
        """Возвращает общее количество всех товаров в корзине пользователя"""

        return sum((basket.quantity for basket in self))

    def get_stripe_price_id(self):
        """Функция для формирования line_items в OrderCreateView при обработке заказа """

        line_items = []
        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity
            }
            line_items.append(item)

        return line_items


class Basket(models.Model):
    """Модель корзины товаров"""

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='корзина для пользователя')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='товар')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='количество товара в корзине')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')

    objects = BasketQuerySet.as_manager()

    class Meta:
        verbose_name = 'корзина товара'
        verbose_name_plural = 'корзины товаров'

    def sum_products(self):
        """Возвращает общую стоиомсть каждого отдельного товара в корзине"""

        return self.quantity * self.product.price

    def history_in_json(self):
        """Заполняет словарь для хранения истории заказа"""

        history_json = {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'total_price': float(self.sum_products())
        }
        return history_json

    def __str__(self):
        return f'{self.user} ||| {self.product}'

    @classmethod
    def create_or_update(cls, product_id, user):
        product = Product.objects.get(id=product_id)
        baskets = Basket.objects.filter(user=user, product=product)

        # если такого товара у пользователя нет, то создаем
        if not baskets.exists():
            basket = Basket.objects.create(
                user=user,
                product=product,
                quantity=1
            )
            create_basket = True

        # иначе добавляем количество данного товара
        else:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()
            create_basket = False

        return basket, create_basket
