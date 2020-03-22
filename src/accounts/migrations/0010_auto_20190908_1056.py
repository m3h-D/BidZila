# Generated by Django 2.2.4 on 2019-09-08 06:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_profile_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidboughts',
            name='amount',
            field=models.IntegerField(default=0, verbose_name='تعداد بیدها'),
        ),
        migrations.AlterField(
            model_name='bidboughts',
            name='bid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bids.Bid', verbose_name='بید'),
        ),
        migrations.AlterField(
            model_name='bidboughts',
            name='ended',
            field=models.BooleanField(default=False, verbose_name='اتمام بید'),
        ),
        migrations.AlterField(
            model_name='bidboughts',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='bidboughts', to='products.Product', verbose_name='محصول'),
        ),
        migrations.AlterField(
            model_name='bidboughts',
            name='title',
            field=models.CharField(max_length=120, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='bidboughts',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bidboughts', to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
    ]
