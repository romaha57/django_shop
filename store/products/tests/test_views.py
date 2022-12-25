from http import HTTPStatus

from django.shortcuts import reverse
from django.test import TestCase

from app_users.models import CustomUser
from products.models import Basket, Product, ProductCategory


class IndexViewTestCase(TestCase):
    """Тест для главной страницы"""

    def test_index_view(self):
        """Тестируем главную страницу"""

        url = reverse('products:index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'products/index.html')
        self.assertEqual(response.context_data['title'], 'Онлайн-магазин')


class ProductListViewTestCase(TestCase):
    """Тест для страницы с каталогом"""

    def setUp(self):
        """Создаем 2 категории и 3 товара"""

        for i in range(2):
            ProductCategory.objects.create(
                name=f'{i} category'
            )

        for i in range(3):
            Product.objects.create(
                name=f'{i} name',
                description=f'{i} description',
                quantity=i,
                price=i,
                image='test_image',
                category=ProductCategory.objects.first()
            )

    def test_list_all_product(self):
        """Тестируем отображение каталога со всеми категориями"""

        url = reverse('products:catalog')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'products/catalog.html')
        self.assertEqual(response.context_data['title'], 'Каталог товаров')

        products = Product.objects.all()
        # делаем списками, чтобы можно было сравнивать
        self.assertEqual(list(response.context_data['object_list']), list(products))

    def test_list_products_with_category(self):
        """Тестируем отображение каталога со определенной категорией"""

        category = ProductCategory.objects.first()
        url = reverse('products:category', kwargs={'category_id': category.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'products/catalog.html')
        self.assertEqual(response.context_data['title'], 'Каталог товаров')
        products = Product.objects.filter(category=category.id)

        # делаем списками, чтобы можно было сравнивать
        self.assertEqual(list(response.context_data['object_list']), list(products))

    def test_list_products_with_pagination(self):
        """Тестируем пагинацию"""

        for i in range(2):
            Product.objects.create(
                name=f'{i} name',
                description=f'{i} description',
                quantity=i,
                price=i,
                image='test_image',
                category=ProductCategory.objects.first()
            )

        url = reverse('products:paginator', kwargs={'page': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'products/catalog.html')
        self.assertEqual(response.context_data['title'], 'Каталог товаров')

        products = Product.objects.all()[:3]

        # проверяем, что на 1 странице отобразилось 3 товара
        self.assertEqual(list(response.context_data['object_list']), list(products))

        url = reverse('products:paginator', kwargs={'page': 2})
        response = self.client.get(url)
        products = Product.objects.all()[3:]

        # проверяем, что на 2 странице отобразилось оставшиеся 2 товара
        self.assertEqual(list(response.context_data['object_list']), list(products))


class BasketAddRemoveTestCase(TestCase):
    """Проверяем добавление и удаление из корзины"""

    def setUp(self):
        """Создаем категорию товара, юзера и товар"""

        ProductCategory.objects.create(
            name='category'
        )

        CustomUser.objects.create(
            first_name='tests',
            last_name='tests',
            username='tests user',
            password='123',
            email='tests@mail.ru'
        )
        Product.objects.create(
            name='name',
            description='description',
            quantity=10,
            price=10,
            image='test_image',
            category=ProductCategory.objects.first()
        )

    def test_add_in_basket_when_basket_not_exists(self):
        """Проверяем создание новой корзины товара"""

        user = CustomUser.objects.first()
        product = Product.objects.first()
        url = reverse('products:add_in_basket', kwargs={'product_id': product.id})
        self.client.get(url)
        baskets = Basket.objects.filter(user=user, product=product)
        if not baskets.exists():
            Basket.objects.create(
                user=user,
                product=product,
                quantity=1
            )
        all_baskets = Basket.objects.all()
        self.assertEqual(len(all_baskets), 1)

    def test_add_in_basket_when_basket_exists(self):
        """Проверяем увелечение количество товара в корзине"""

        user = CustomUser.objects.first()
        product = Product.objects.first()
        basket = Basket.objects.create(
            user=user,
            product=product,
            quantity=1
        )

        url = reverse('products:add_in_basket', kwargs={'product_id': product.id})
        self.client.get(url)
        baskets = Basket.objects.filter(user=user, product=product)
        if baskets.exists():
            basket.quantity += 1
            basket.save()

        self.assertEqual(basket.quantity, 2)
