# Generated by Django 4.2.2 on 2023-06-29 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_seating_is_empty'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='poster',
            field=models.TextField(default='None'),
        ),
    ]
