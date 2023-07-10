# Generated by Django 4.2.2 on 2023-07-10 08:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('data', '0009_transactionrecord_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fund',
            name='id',
        ),
        migrations.AddField(
            model_name='fund',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
