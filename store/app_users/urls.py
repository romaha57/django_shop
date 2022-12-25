from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (EmailVerifyView, UserLoginView, UserProfileView,
                    UserRegistrationView)

# namespace for users app
app_name = 'app_users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('profile/<int:pk>', UserProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify_email/<str:email>/<uuid:unique_code>', EmailVerifyView.as_view(), name='verify_email'),
]
