from django.shortcuts import render
from data.models import Movie
from data.models import Fund

# Create your views here.
def home_view(request, *args, **kwargs):
    logged_in = request.user.is_authenticated
    # get a movie object
    movies = Movie.objects.all()
    balance = Fund.objects.get(pk=1).current_fund
    return render(request, "home.html", {
        "movies" : movies,
        "fund" : format(balance, ","),
        "logged_in" : logged_in,
        "username" : request.user.username
    })


