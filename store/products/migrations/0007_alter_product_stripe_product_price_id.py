# Generated by Django 3.2.16 on 2022-12-23 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_product_stripe_product_price_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='stripe_product_price_id',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='price id для stripe'),
        ),
    ]