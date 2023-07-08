from django.shortcuts import render
from data.models import Fund
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib import messages

# Create your views here.
def login_user(request):
    balance = getBalance()
    if request.method == "GET":
        return render(request, "login.html", {
            "fund" : format(balance, ',')
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
                "fund" : format(balance, ',')
            })

def logout_user(request):
    # POST only
    logout(request)
    return HttpResponseRedirect("/")

def getBalance():
    return Fund.objects.get(pk=1).current_fund