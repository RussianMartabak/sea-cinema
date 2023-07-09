from django.shortcuts import render
from data.models import Fund
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import User

# Create your views here.
def login_user(request):
    balance = getBalance(request)
    if request.method == "GET":
        return render(request, "login.html", {
            "fund" : balance
        })
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            messages.error(request, "Incorrect username or password. I won't tell you which because I'm lazy lol")
            return render(request, "login.html", {
                
            })

def logout_user(request):
    # POST only
    logout(request)
    return HttpResponseRedirect("/")

def register_user(request):
    if request.method =="GET":
        return render(request, "register.html", {})
    elif request.method == "POST":
        name = request.POST["name"]
        username = request.POST["username"]
        age = request.POST["age"]
        password = request.POST["password"]
        if len(User.objects.filter(username=username)) != 0:
            # error
            messages.error(request, "Username taken")
            return render(request, "register.html", {})
        else:
            # success
            new_user = User.objects.create_user(name=name, username=username, age=age, password=password)
            new_user.save()
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return HttpResponseRedirect("/")

            


def getBalance(request):
    # return formatted String
    fund = Fund.objects.get(pk=1).current_fund
    return format(fund, ',')