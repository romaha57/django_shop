from django.urls import path

from .views import loginn, registration, profile, logoutt

app_name = 'app_users'

urlpatterns = [
    path('login/', loginn, name='login'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
    path('logoutt/', logoutt, name='logout'),
]