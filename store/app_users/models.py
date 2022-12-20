from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail

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

    def send_email_for_verification_user(self):
        send_mail(
            subject='тема',
            message='текст письма',
            from_email='test@mai.ru',
            recipient_list=[self.user.email]
        )


