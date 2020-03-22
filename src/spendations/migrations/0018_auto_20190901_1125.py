# Generated by Django 2.2.4 on 2019-09-01 06:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('spendations', '0017_auto_20190830_1934'),
    ]

    operations = [
        migrations.AddField(
            model_name='spend',
            name='last_spend',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 1, 6, 55, 15, 794285, tzinfo=utc), verbose_name='زمان اخرین پیشنهاد'),
        ),
        migrations.AlterField(
            model_name='spend',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 1, 6, 55, 15, 795281, tzinfo=utc), verbose_name='اتمام زمان توان خرید'),
        ),
    ]