# Generated by Django 4.2.5 on 2024-01-23 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_productimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=155, unique=True, verbose_name='Название продукта'),
        ),
    ]
