# Generated by Django 2.2.4 on 2019-08-21 13:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('spendations', '0004_auto_20190821_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spend',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 21, 13, 14, 24, 885237, tzinfo=utc), verbose_name='اتمام زمان توان خرید'),
        ),
    ]
