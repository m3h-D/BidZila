# Generated by Django 2.2.4 on 2019-08-21 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='final_prices',
            new_name='final_price',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='new_prices',
            new_name='new_price',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='true_prices',
            new_name='true_price',
        ),
    ]