from django.shortcuts import render
from data.models import Movie
from data.models import Fund
from django.http import HttpResponseRedirect
from data.models import Seating



# Create your views here.
def movie_detail(request, *args, **kwargs):
    balance = getBalance()
    movie_object = Movie.objects.get(pk=kwargs["movie_id"])
    payload = {"movie" : movie_object, "fund" : format(balance, ','), 
        "price" : format(movie_object.ticket_price, ',')}
    return render(request, "movie_detail.html", payload)

def balance(request, *args, **kwargs):
    balance = getBalance()
    return render(request, "balance_detail.html", {
        "fund" : format(balance, ','),
        "fund_numeric" : balance
    })


def topup(request):
    topup_amount = request.POST["topupAmount"].replace(".", "")
    balance = Fund.objects.get(pk=1)
    balance.current_fund += int(topup_amount)
    balance.save()
    return HttpResponseRedirect('/')

def withdraw(request):
    withdraw_amount = int(request.POST["withdrawAmount"].replace(".",""))
    balance = Fund.objects.get(pk=1)
    if withdraw_amount <= balance.current_fund:
        balance.current_fund -= int(withdraw_amount)
        balance.save()
    return HttpResponseRedirect('/')
    
def get_booking(request, movie_id):
    request.session['movie_id'] = movie_id
    balance = getBalance()
    movie_seats = []
    movie_title = Movie.objects.get(pk=movie_id).title
    movie_age = Movie.objects.get(pk=movie_id).age_rating
    # make 2 dimensional list (list containing list) a list of row containing seats
    data_movie_seats = Seating.objects.filter(movie_id_id=movie_id)
    current_indice = 0
    for i in range(8):
        new_array = []
        for j in range(8):
            new_array.append(data_movie_seats[current_indice])
            current_indice += 1
        movie_seats.append(new_array)
    # filter based on foreign key
    
    return render(request, "booking.html", {
        "fund" : format(balance, ','),
        "movie_title" : movie_title,
        "movie_seats" : movie_seats,
        "movie_age" : movie_age
    })

def payment(request):
    test_data = request.session.get('test_data')
    return render(request, "payment.html", {
        "test_data" : test_data
    })

# helpers

def post_booking(request):
    request.session['test_data'] = request.POST
    return HttpResponseRedirect('/')
    
def getBalance():
    
    return Fund.objects.get(pk=1).current_fund