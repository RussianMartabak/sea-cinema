from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    name = models.TextField(default="a")
    username = models.TextField(unique=True)
    age = models.IntegerField(default=0)
    password = models.TextField()