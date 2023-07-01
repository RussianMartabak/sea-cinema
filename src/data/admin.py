from django.contrib import admin
from .models import Fund
from .models import Movie
from .models import Seating

# Register your models here.
admin.site.register(Fund)
admin.site.register(Movie)
admin.site.register(Seating)