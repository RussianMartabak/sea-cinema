# Generated by Django 4.2.2 on 2023-06-29 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_seating_movie_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='ticket_price',
            field=models.IntegerField(default=75000),
        ),
    ]
