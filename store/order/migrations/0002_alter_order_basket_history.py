# Generated by Django 3.2.16 on 2022-12-22 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='basket_history',
            field=models.JSONField(default=dict, verbose_name='история корзины'),
        ),
    ]
