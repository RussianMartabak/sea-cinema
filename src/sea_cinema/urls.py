"""
URL configuration for sea_cinema project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home.views import home_view
from pages.views import movie_detail
from pages.views import balance
from pages.views import topup
from pages.views import withdraw
from pages.views import get_booking
from pages.views import post_booking
from pages.views import payment
from pages.views import refund
from users.views import login_user, logout_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='main'),
    path("movie/<int:movie_id>", movie_detail),
    path("balance", balance, name="balance"),
    path("topup", topup),
    path("withdraw", withdraw),
    path("booking/<int:movie_id>", get_booking, name="booking"), 
    path("booking", post_booking),
    path("payment", payment),
    path("refund", refund),
    path("login", login_user, name="login"),
    path("logout", logout_user, name="logout"),
]
