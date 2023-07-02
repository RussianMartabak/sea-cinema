from django.shortcuts import render
from data.models import Movie
from data.models import Fund
from django.http import HttpResponseRedirect
from data.models import Seating
from django.http import HttpResponse


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
    balance = getBalance()
    booking_data = request.session.get('booking_data')
    #this make booked seats into proper sequence of numbers
    booked_seats = convertToArray(booking_data["booked_seats"]) 
    #movie_id is already saved on session
    movie_id = request.session['movie_id']
    quantity = len(booked_seats)
    total_price = getTotalPrice(len(booked_seats), movie_id)
    # pack all this things (name, total price, quantity, movie_id into a dictionary and put it in session)
    # it all will be used in the POST request (redirect to home too)
    order_data = {}
    order_data['movie_title'] = Movie.objects.get(pk=movie_id).title
    order_data['name'] = booking_data["name"]
    order_data['total_price'] = total_price
    order_data['quantity'] = quantity
    request.session['order_data'] = order_data

    if request.method == "GET":
        return render(request, "payment.html", {
            "booking_seats" : booked_seats,
            "name" : booking_data["name"],
            "fund" : format(balance, ','),
            "total_price" : total_price,
            "movie_title" : Movie.objects.get(pk=movie_id).title,
            "quantity" : quantity,
            'ticket_price' : Movie.objects.get(pk=movie_id).ticket_price
        })
    elif request.method == "POST":
        order_data = request.session['order_data']
        if order_data['total_price'] > balance:
            return HttpResponse("epic fail")

# helpers

def post_booking(request):
    request.session['booking_data'] = request.POST
    return HttpResponseRedirect('/')
    
def getBalance():
    
    return Fund.objects.get(pk=1).current_fund

def convertToArray(string):
    cs_string = string.replace('\n', '').replace('\r', '').replace(' ', '')
    num_array = cs_string.split(',')
    return num_array

def getTotalPrice(qty, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    return movie.ticket_price * qty