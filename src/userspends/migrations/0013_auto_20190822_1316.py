# Generated by Django 2.2.4 on 2019-08-22 08:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('userspends', '0012_auto_20190822_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userspend',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 22, 8, 46, 46, 311204, tzinfo=utc)),
        ),
    ]
