from rest_framework import fields, serializers

from products.models import Basket, Product, ProductCategory


class ProductSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Товаров"""

    category = serializers.SlugRelatedField(slug_field='name', queryset=ProductCategory.objects.all())

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'quantity', 'price', 'category')


class BasketSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Корзина"""

    product = ProductSerializer()
    sum_products = fields.FloatField(required=False)
    total_sum = serializers.SerializerMethodField()
    total_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Basket
        fields = ('id', 'product', 'quantity', 'sum_products', 'total_sum', 'total_quantity', 'created_at')

    def get_total_sum(self, obj):
        """Функция для добавления поля общей суммы всей корзины"""

        return Basket.objects.filter(user=obj.user).total_sum()

    def get_total_quantity(self, obj):
        """Функция для добавления поля общего количества всей корзины"""

        return Basket.objects.filter(user=obj.user).total_quantity()
