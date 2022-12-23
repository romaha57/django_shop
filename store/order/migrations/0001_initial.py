# Generated by Django 3.2.16 on 2022-12-22 21:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=128, verbose_name='имя')),
                ('last_name', models.CharField(max_length=128, verbose_name='фамилия')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('address', models.CharField(max_length=255, verbose_name='адрес')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('basket_history', models.JSONField(verbose_name='история корзины')),
                ('status', models.SmallIntegerField(choices=[(1, 'создан'), (2, 'оплачен'), (3, 'в пути'), (4, 'выполнен')], default=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='покупатель')),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'заказы',
            },
        ),
    ]
