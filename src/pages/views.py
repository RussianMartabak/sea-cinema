from django.shortcuts import render
from data.models import Movie
from data.models import Fund
from django.http import HttpResponseRedirect
from data.models import Seating
from django.http import HttpResponse
from data.models import TransactionRecord


# Create your views here.
def movie_detail(request, *args, **kwargs):
    balance = getBalance(request)
    logged_in = request.user.is_authenticated
    if balance:
        balance = format(balance.current_fund, ',')
    movie_object = Movie.objects.get(pk=kwargs["movie_id"])
    payload = {"movie" : movie_object, "fund" : balance, 
        "price" : format(movie_object.ticket_price, ','),
        "logged_in" : logged_in,
        "username" : request.user.username
        }
    return render(request, "movie_detail.html", payload)

def balance(request, *args, **kwargs):
    logged_in = request.user.is_authenticated
    if logged_in:
        balance = Fund.objects.get(user__pk=request.user.id).current_fund
        transactions = TransactionRecord.objects.all()
        return render(request, "balance_detail.html", {
            "fund" : format(balance, ','),
            "fund_numeric" : balance,
            "transactions" : transactions
        })
    else:
        return HttpResponseRedirect("/login")


def topup(request):
    topup_amount = request.POST["topupAmount"].replace(".", "")
    balance = getBalance(request)
    balance.current_fund += int(topup_amount)
    balance.save()
    return HttpResponseRedirect('/')

def withdraw(request):
    withdraw_amount = int(request.POST["withdrawAmount"].replace(".",""))
    balance = getBalance(request)
    if withdraw_amount <= balance.current_fund:
        balance.current_fund -= int(withdraw_amount)
        balance.save()
    return HttpResponseRedirect('/')
    
def get_booking(request, movie_id):
    if request.user.is_authenticated:
        request.session['movie_id'] = movie_id
        balance = getBalance(request).current_fund #fund object, remember this
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
            "movie_age" : movie_age,
            "logged_in" : request.user.is_authenticated,
            "username" : request.user.username
        })
    else:
        return HttpResponseRedirect("/login")

def payment(request):
    if request.user.is_authenticated:
        balance = getBalance(request).current_fund
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
        order_data['total_price'] = total_price
        order_data['quantity'] = quantity
        order_data['booked_seats'] = booked_seats
        order_data['movie_id'] = movie_id
        request.session['order_data'] = order_data

        if request.method == "GET":
            return render(request, "payment.html", {
                "booking_seats" : booked_seats,
                "name" : request.user.name,
                "fund" : format(balance, ','),
                "total_price" : total_price,
                "movie_title" : Movie.objects.get(pk=movie_id).title,
                "quantity" : quantity,
                'ticket_price' : Movie.objects.get(pk=movie_id).ticket_price,
                'logged_in' : True,
                'username' : request.user.username
            })
        elif request.method == "POST":
            order_data = request.session['order_data']
            if order_data['total_price'] > balance:
                return HttpResponse("epic fail")
            else:
                # fill in the seats and also the transaction records
                # deduct from balance
                current_balance = Fund.objects.get(pk=1)
                current_balance.current_fund -= order_data['total_price']
                current_balance.save()
                #book the seat
                booked_seats = order_data['booked_seats']
                movie_id = order_data['movie_id']
                movie_seats = Seating.objects.filter(movie_id_id = movie_id)
                for seat in booked_seats:
                    # search based on seat number and movie id
                    target_seat = movie_seats.filter(seat_number=seat)[0]
                    target_seat.is_empty = False
                    target_seat.save()
                # now record the transactions
                transaction = TransactionRecord(
                total = order_data['total_price'],
                seats = stringify(booked_seats), 
                name = order_data['name'],
                quantity = order_data['quantity'],
                title = order_data['movie_title']
                )
                transaction.save()

                return HttpResponse("success")
        else:
            return HttpResponseRedirect("/login")

# helpers

def post_booking(request):
    # age restrict first
    movie_id = request.session["movie_id"]
    movie_age_rating = Movie.objects.get(id=movie_id).age_rating
    if request.user.age < movie_age_rating:
        return HttpResponse('fail')
    else:
        request.session['booking_data'] = request.POST
        return HttpResponse('succ')

def refund(request):
    transaction_id = request.POST["transaction_id"]
    transaction_entry = TransactionRecord.objects.get(pk=transaction_id)
    balance = Fund.objects.get(pk=1)
    balance.current_fund += transaction_entry.total
    balance.save()
    #get the seats in the database 
    # first get movie_id
    movie = Movie.objects.get(title = transaction_entry.title)
    movie_id = movie.id
    # now get the seats from transaction records
    refunded_seats = StringArraytoNumArray(transaction_entry.seats.split(','))
    movie_seats = Seating.objects.filter(movie_id_id = movie_id)
    # now change all the seat in db
    print(refunded_seats)
    for refund_seat in refunded_seats:
        seat = movie_seats.filter(seat_number=refund_seat)
        print(seat)
        target_seat = seat[0]
        target_seat.is_empty = True
        target_seat.save()
    #delete trans entry
    transaction_entry.delete()
    return HttpResponseRedirect('/')


def getBalance(request):
    # return fund object on that user if not found return None
    if request.user.is_authenticated:
        fund = Fund.objects.get(user__pk=request.user.id)
        return fund
    else:
        return None

def convertToArray(string):
    cs_string = string.replace('\n', '').replace('\r', '').replace(' ', '')
    num_array = cs_string.split(',')
    return num_array

def getTotalPrice(qty, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    return movie.ticket_price * qty

def stringify(array):
    res = ""
    for i in array:
        res += i + ", "
    return res

def StringArraytoNumArray(array):
    res = []
    for item in array:
        if item.strip().isnumeric():
            res.append(int(item.strip()))
    return res
