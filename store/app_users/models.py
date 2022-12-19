from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='images_for_user', null=True, blank=True)