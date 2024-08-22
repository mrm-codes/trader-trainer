from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # type: ignore
from django.contrib.auth import login, authenticate # type: ignore
from .forms import RegisterUserForm, LoginUserForm

#Trading requirements
import yahoo_fin.stock_info as si
import yfinance as yf
import time
import requests
from .models import Portfolio, Holdings, Transaction, Overview


# Create your views here.
def base(request):
    return render(request, 'base.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def faq(request):
    return render(request, 'faq.html')

def login_user(request):
    form = LoginUserForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/user_dash') # user dash
    return render(request, 'login_form.html', {'form': form})

def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)           
            return redirect ('/login_user')

    else:
        form = RegisterUserForm()       
    return render(request, 'registration_form.html', {'form': form,})

#Trading Views


def user_dash(request):
        ticker = Overview.ticker
        bid = Overview.bid
        ask = Overview.ask
        price = Overview.price
        context= {
            'ticker': ticker,
            'bid': bid,
            'ask': ask,
            'price': price,
            'daily change': Overview.daily_change_percent, 
        }

        return render(request, 'user_dashboard.html', context)

  

