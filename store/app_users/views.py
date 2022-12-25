from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from app_users.models import CustomUser, VerifyEmailModel
from products.models import Basket
from utils.mixins import TitleMixin

from .forms import LoginForm, ProfileForm, RegistrationForm


class UserLoginView(TitleMixin, LoginView):
    """Логин пользователя"""

    form_class = LoginForm
    template_name = 'app_users/login.html'
    title = 'Вход'


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    """Регистрация пользователя"""

    model = CustomUser
    form_class = RegistrationForm
    template_name = 'app_users/registration.html'
    success_url = reverse_lazy('app_users:login')
    title = 'Регистрация'
    success_message = 'Вы успешно зарегистрировались. На указанную почту было выслано письмо для подтвеждения'


class UserProfileView(TitleMixin, LoginRequiredMixin, UpdateView):
    """Отображение личного кабинета пользователя"""

    model = CustomUser
    form_class = ProfileForm
    template_name = 'app_users/profile.html'
    title = 'Личный кабинет'

    def get_success_url(self):
        """Формирование ссылки при переходе в личный кабинет"""

        return reverse_lazy('app_users:profile', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        """Формирование корзины пользователя для отображения в личном кабинете"""

        context = super().get_context_data(**kwargs)
        context['basket'] = Basket.objects.filter(user=self.request.user)

        return context


class EmailVerifyView(TitleMixin, TemplateView):
    """Страница при подтвеждении почты"""

    title = 'Подтверждение почты'
    template_name = 'app_users/email_verification.html'

    def get(self, request, *args, **kwargs):
        """Переопределяем метод get для подтверждения почты"""

        unique_code = kwargs.get('unique_code')
        user = CustomUser.objects.get(email=kwargs.get('email'))
        records = VerifyEmailModel.objects.filter(user=user, unique_code=unique_code)

        # если запись о подтвеждении почты есть и срок действия ссылки не истек, то верифицируем почту
        if records.exists() and records.first().is_expired():
            user.email_is_verified = True
            user.save()
            return super().get(request, *args, **kwargs)
        else:
            return redirect('products:index')
