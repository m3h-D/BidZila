# Generated by Django 2.2.4 on 2019-08-22 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_secret_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='secret_key',
            field=models.CharField(blank=True, max_length=200, verbose_name='کد'),
        ),
    ]
