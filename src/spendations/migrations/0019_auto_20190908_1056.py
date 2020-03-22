# Generated by Django 2.2.4 on 2019-09-08 06:26

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('spendations', '0018_auto_20190901_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spend',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 8, 6, 26, 30, 484929, tzinfo=utc), verbose_name='اتمام زمان توان خرید'),
        ),
        migrations.AlterField(
            model_name='spend',
            name='last_spend',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 8, 6, 26, 30, 484929, tzinfo=utc), verbose_name='زمان اخرین پیشنهاد'),
        ),
    ]
