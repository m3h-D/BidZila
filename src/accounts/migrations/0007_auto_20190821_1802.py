# Generated by Django 2.2.4 on 2019-08-21 13:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_profile_have_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidboughts',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bidboughts', to=settings.AUTH_USER_MODEL),
        ),
    ]
