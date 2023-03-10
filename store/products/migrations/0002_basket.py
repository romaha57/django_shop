# Generated by Django 3.2.16 on 2022-12-19 17:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.SmallIntegerField(default=0, verbose_name='количество товара в корзине')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='товар')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='корзина для пользователя')),
            ],
            options={
                'verbose_name': 'корзина товара',
                'verbose_name_plural': 'корзины товаров',
            },
        ),
    ]
