import uuid
from http import HTTPStatus

from app_users.models import CustomUser, VerifyEmailModel
from django.shortcuts import reverse
from django.test import TestCase


class UserRegistrationViewTestCase(TestCase):
    def setUp(self):
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
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'app_users/registration.html')
        self.assertEqual(response.context_data['title'], 'Регистрация')

    def test_registration_user_post_success(self):

        users = CustomUser.objects.all()
        self.assertFalse(users.exists())

        response = self.client.post(self.url, self.correct_user_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('app_users:login'))

        users = CustomUser.objects.all()
        self.assertTrue(users.exists())

        email_verify = VerifyEmailModel.objects.all()
        self.assertTrue(email_verify.exists())

    def test_registration_user_post_error(self):
        CustomUser.objects.create(username=self.correct_user_data['username'])
        response = self.client.post(self.url, self.correct_user_data)
        self.assertContains(response, 'Пользователь с таким именем уже существует')


class UserLoginViewTestCase(TestCase):
    def setUp(self):
        CustomUser.objects.create(
            first_name='testsusername',
            last_name='testsfirst_name',
            username='testsuser_name',
            email='test@mail.ru',
            password='Qweasdfgh123',
        )
        self.url = reverse('app_users:login')

    def test_login_user_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'app_users/login.html')
        self.assertEqual(response.context_data['title'], 'Вход')

    def test_login_user_post_success(self):
        user = CustomUser.objects.first()
        self.client.force_login(user=user)
        response = self.client.get(reverse('products:index'))
        self.assertEqual(str(response.context['user']), user.username)

    def test_login_user_post_error(self):
        incorrect_data_for_login = {
            'username': 'error',
            'password': 'error'
        }
        response = self.client.post(self.url, incorrect_data_for_login)
        self.assertContains(response, 'Пожалуйста, введите правильные имя')


class UserProfileViewTestCase(TestCase):
    def setUp(self):
        user = CustomUser.objects.create(
            first_name='testsusername',
            last_name='testsfirst_name',
            username='testsuser_name',
            email='test@mail.ru',
            password='Qweasdfgh123',
        )

        self.url = reverse('app_users:profile', args=(user.id,))

    def test_user_profile_get(self):
        user = CustomUser.objects.first()
        self.client.force_login(user=user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'app_users/profile.html')
        self.assertEqual(response.context_data['title'], 'Личный кабинет')

    def test_user_profile_post_success(self):
        user = CustomUser.objects.first()
        self.client.force_login(user=user)
        response = self.client.post(self.url, {'username': 'new'})
        self.assertEqual(str(response.context_data['customuser']), 'new')


class EmailVerifyViewTestCase(TestCase):
    def setUp(self):
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
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('products:index'))
