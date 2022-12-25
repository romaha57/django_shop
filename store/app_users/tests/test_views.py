import uuid
from http import HTTPStatus

from django.shortcuts import reverse
from django.test import TestCase

from app_users.models import CustomUser, VerifyEmailModel


class UserRegistrationViewTestCase(TestCase):
    """Тестируем форму регистрации пользователя"""

    def setUp(self):
        """Создаем корректные данные для регистрации пользователя"""

        self.correct_user_data = {
            'first_name': 'testsusername',
            'last_name': 'testsfirst_name',
            'username': 'testslast_name',
            'email': 'test@mail.ru',
            'password1': 'Qweasdfgh123',
            'password2': 'Qweasdfgh123',

        }
        self.url = reverse('app_users:registration')

    def test_registration_user_get(self):
        """Тестируем get запрос на страницу регистрации"""

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'app_users/registration.html')
        self.assertEqual(response.context_data['title'], 'Регистрация')

    def test_registration_user_post_success(self):
        """Тестируем post запрос при успешной регистрации пользователя"""

        # проверяем что пользователя в бд нет
        users = CustomUser.objects.all()
        self.assertFalse(users.exists())

        response = self.client.post(self.url, self.correct_user_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('app_users:login'))

        # проверяем что пользователь создался
        users = CustomUser.objects.all()
        self.assertTrue(users.exists())

        # проверяем что создалась модель для подтверждения почты
        email_verify = VerifyEmailModel.objects.all()
        self.assertTrue(email_verify.exists())

    def test_registration_user_post_error(self):
        """Тестируем проверку на уникальность поля username"""

        CustomUser.objects.create(username=self.correct_user_data['username'])
        response = self.client.post(self.url, self.correct_user_data)
        self.assertContains(response, 'Пользователь с таким именем уже существует')


class UserLoginViewTestCase(TestCase):
    """Тестируем логин пользователя"""

    def setUp(self):
        """Создаем пользователя в БД"""

        CustomUser.objects.create(
            first_name='testsusername',
            last_name='testsfirst_name',
            username='testsuser_name',
            email='test@mail.ru',
            password='Qweasdfgh123',
        )
        self.url = reverse('app_users:login')

    def test_login_user_get(self):
        """Тестируем get запрос на страницу логина"""

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'app_users/login.html')
        self.assertEqual(response.context_data['title'], 'Вход')

    def test_login_user_post_success(self):
        """Тестируем post запрос на страницу логина и перенаправление на главную страницу при успехе"""

        user = CustomUser.objects.first()
        self.client.force_login(user=user)
        response = self.client.get(reverse('products:index'))
        self.assertEqual(str(response.context['user']), user.username)

    def test_login_user_post_error(self):
        """Тестируем post запрос на страницу логина и выдачу ошибки при аутентификации пользователя"""

        incorrect_data_for_login = {
            'username': 'error',
            'password': 'error'
        }
        response = self.client.post(self.url, incorrect_data_for_login)
        self.assertContains(response, 'Пожалуйста, введите правильные имя')


class UserProfileViewTestCase(TestCase):
    """Тестируем личный кабинет пользователя"""

    def setUp(self):
        """Создаем пользователя"""

        user = CustomUser.objects.create(
            first_name='testsusername',
            last_name='testsfirst_name',
            username='testsuser_name',
            email='test@mail.ru',
            password='Qweasdfgh123',
        )

        self.url = reverse('app_users:profile', args=(user.id,))

    def test_user_profile_get(self):
        """Тестируем get запрос на страницу личного кабинета"""

        user = CustomUser.objects.first()
        self.client.force_login(user=user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'app_users/profile.html')
        self.assertEqual(response.context_data['title'], 'Личный кабинет')

    def test_user_profile_post_success(self):
        """Тестируем изменение данных о пользователе в личном кабинете"""

        user = CustomUser.objects.first()
        self.client.force_login(user=user)
        response = self.client.post(self.url, {'username': 'new'})
        self.assertEqual(str(response.context_data['customuser']), 'new')


class EmailVerifyViewTestCase(TestCase):
    """Тестируем верификацию почты"""

    def setUp(self):
        """Создаем пользователя"""

        self.user = CustomUser.objects.create(
            first_name='testsusername',
            last_name='testsfirst_name',
            username='testsuser_name',
            email='test@mail.ru',
            password='Qweasdfgh123',
        )

        self.code = uuid.uuid4()

        self.url = reverse('app_users:verify_email', kwargs={
            'email': self.user.email,
            'unique_code': self.code
        })

    def test_email_verify_view_get_error(self):
        """Тестируем перенаправление на главную страницу при ошибке подтверждения почты"""

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('products:index'))
