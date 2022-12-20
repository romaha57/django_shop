from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='images_for_user', null=True, blank=True)
    email_is_verified = models.BooleanField(default=False, verbose_name='подтверждена почта?')


class VerifyEmailModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='пользователь')
    unique_code = models.UUIDField(unique=True, verbose_name='уникальный код для создания ссылки подтверждения почты')
    experation_link = models.DateTimeField(verbose_name='срок жизни ссылки')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'подтверждение почты'
        verbose_name_plural = 'подтверждения почт'

    def __str__(self):
        return f'{self.user.username}'

    def is_expired(self):
        return True if now() <= self.experation_link else False

    def send_email_for_verification_user(self):
        link = reverse('app_users:verify_email', kwargs={'email': self.user.email, 'unique_code': self.unique_code})
        full_link = settings.DOMAIN_NAME + link
        subject = 'Письмо для подтверждения электронной почты'
        message = f'Для подтверждения эл. почты {self.user.email} перейдите по ссылке: {full_link}'
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email]
        )
