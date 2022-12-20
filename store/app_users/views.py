from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import LoginForm, RegistrationForm, ProfileForm
from products.models import Basket
from app_users.models import CustomUser
from utils.mixins import TitleMixin


class UserLoginView(TitleMixin, LoginView):
    form_class = LoginForm
    template_name = 'app_users/login.html'
    title = 'Вход'


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = RegistrationForm
    template_name = 'app_users/registration.html'
    success_url = reverse_lazy('app_users:login')
    title = 'Регистрация'
    success_message = 'Вы успешно зарегистрировались'


class UserProfileView(TitleMixin, LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileForm
    template_name = 'app_users/profile.html'
    title = 'Личный кабинет'

    def get_success_url(self):
        return reverse_lazy('app_users:profile', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basket'] = Basket.objects.filter(user=self.object)
        return context
