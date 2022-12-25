from rest_framework import status
from rest_framework.permissions import (IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from products.models import Basket, Product

from .serializers import BasketSerializer, ProductSerializer


class ProductModelViewSet(ModelViewSet):
    """Отображение товаров"""

    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_permissions(self):
        """Разрешаем только администратору добавлять, обновлять и удалять товары"""

        if self.action in ('create', 'destroy', 'update'):
            self.permission_classes = (IsAdminUser,)
        return super().get_permissions()


class BasketModelViewSet(ModelViewSet):
    """Отображене корзины"""

    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        """Формируем queryset корзины для конкретного пользователя"""

        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Переопределяем метод для возможности добавления товаров в корзину"""

        try:
            product_id = request.data['product_id']
            products = Product.objects.filter(id=product_id)

            if not products.exists():
                return Response({'error': 'Продукта с таким id нет в базе данных'}, status=status.HTTP_400_BAD_REQUEST)

            basket, create_basket = Basket.create_or_update(product_id, request.user)

            # если такого товара не было в корзине
            if create_basket:
                status_code = status.HTTP_201_CREATED

            # если такой товар был в корзине
            else:
                status_code = status.HTTP_200_OK
            serializer = self.get_serializer(basket)

            return Response(serializer.data, status=status_code)

        except KeyError:
            return Response({'error': 'product_id is not found'})
