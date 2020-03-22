# Generated by Django 2.2.4 on 2019-08-28 11:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('spendations', '0015_auto_20190827_1732'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spend',
            name='def_offer',
        ),
        migrations.AlterField(
            model_name='spend',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 28, 11, 51, 43, 324537, tzinfo=utc), verbose_name='اتمام زمان توان خرید'),
        ),
        migrations.AlterField(
            model_name='spend',
            name='email_send',
            field=models.BooleanField(default=False, verbose_name='ایمیل فرستاده شده'),
        ),
        migrations.AlterField(
            model_name='spend',
            name='user_can',
            field=models.BooleanField(default=False, verbose_name='برنده'),
        ),
        migrations.AlterField(
            model_name='spend',
            name='user_ended',
            field=models.BooleanField(default=False, verbose_name='خریداری کرده'),
        ),
        migrations.AlterField(
            model_name='spend',
            name='user_won',
            field=models.BooleanField(default=False, verbose_name='ثبت بعنوان برنده اصلی محصول'),
        ),
    ]