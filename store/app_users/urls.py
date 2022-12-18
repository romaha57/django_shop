from django.urls import path

from .views import loginn, registration

app_name = 'app_users'

urlpatterns = [
    path('login/', loginn, name='login'),
    path('registration/', registration, name='registration')
]