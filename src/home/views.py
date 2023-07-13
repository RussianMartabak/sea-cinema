from django.shortcuts import render
from data.models import Movie
from data.models import Fund

# Create your views here.
def home_view(request, *args, **kwargs):
    logged_in = request.user.is_authenticated
    # get a movie object
    movies = Movie.objects.all()
    # if not logged in empty balance
    if logged_in:
        balance = Fund.objects.get(user__pk=request.user.id).current_fund
        balance = format(balance, ",")
    else:
        balance = None
    return render(request, "home.html", {
        "movies" : movies,
        "fund" : balance,
        "logged_in" : logged_in,
        "username" : request.user.username
    })


