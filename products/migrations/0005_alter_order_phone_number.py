# Generated by Django 5.1.5 on 2025-02-03 07:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_stock_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='phone_number',
            field=models.CharField(blank=True, max_length=13, null=True, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format: +998xxxxxxxxx.', regex='^\\+998\\d{9}$')]),
        ),
    ]
