# Generated by Django 2.2.4 on 2019-08-21 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='have_bid',
            field=models.ManyToManyField(related_name='profile', to='accounts.BidBoughts', verbose_name='تعداد بید ها'),
        ),
    ]
