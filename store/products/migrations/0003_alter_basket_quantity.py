# Generated by Django 3.2.16 on 2022-12-19 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_basket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='количество товара в корзине'),
        ),
    ]
