# Generated by Django 2.2.4 on 2019-08-21 09:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('userspends', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userspend',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 21, 9, 12, 31, 264260, tzinfo=utc)),
        ),
    ]
