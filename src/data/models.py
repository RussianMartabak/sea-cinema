from django.db import models
from users.models import User

# Create your models here.

class Fund(models.Model):
    current_fund = models.IntegerField(default=0)
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        primary_key=True,
        default = 1
    )

class Movie(models.Model):
    title = models.TextField()
    age_rating = models.IntegerField(default=18)
    storyline = models.TextField()
    ticket_price = models.IntegerField(default=75000)
    genre = models.TextField(default="Action")
    poster = models.TextField(default="None")

class Seating(models.Model):
    seat_number = models.IntegerField()
    is_empty = models.BooleanField(default=True)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE, default = 1)

class TransactionRecord(models.Model):
    total = models.IntegerField()
    seats = models.TextField()
    name = models.TextField()
    title = models.TextField()
    quantity = models.IntegerField(default=1)
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        primary_key=True,
        default = 1
    )
