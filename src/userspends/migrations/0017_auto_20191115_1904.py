# Generated by Django 2.2.4 on 2019-11-15 15:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('userspends', '0016_auto_20190908_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userspend',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 15, 15, 34, 7, 85996, tzinfo=utc)),
        ),
    ]
