# Generated by Django 2.2.4 on 2019-08-28 11:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('userspends', '0014_auto_20190825_0142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userspend',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 28, 11, 51, 43, 325536, tzinfo=utc)),
        ),
    ]
