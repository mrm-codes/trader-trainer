from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # type: ignore
from django.contrib.auth import login, authenticate # type: ignore
from .forms import RegisterUserForm, LoginUserForm

#Trading requirements
import yahoo_fin.stock_info as si
import yfinance as yf
import time
import requests
from .models import Portfolio, Holdings, Transaction



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
    #stock data info
    while True:
        def stock_data(ticker):
            stock = yf.Ticker(ticker)
            data_history = stock.history(period='1d', interval='1m ')
            message = 'No data to display'
            if not data_history.empty:
                # Get the opening price (first price of the day)
                opening_price = data_history['Open'][0]
                
                # Get the current or last close price (latest price of the day)
                current_price = data_history['Close'].iloc[-1]   
                price = round(current_price, 2)
                
                #gettin the current bid
                on_price = stock.info.get('bid', 'No data available')
                bid = round(on_price, 2)

                #Getting the gurrent ask
                off_price = stock.info.get('ask', 'No data available')
                ask = round(off_price, 2)

                # Calculate daily change percentage
                daily_change_percentage = ((current_price - opening_price) / opening_price) * 100
                daily_change = round(daily_change_percentage, 2)
            else:
                print(message)
            
            return  {'ticker': 'ticker',
                    'bid': 'bid',
                    'ask': 'ask',
                    'price': 'price',
                    'daily_change':' daily_change',
                    }
        
        aapl = stock_data('AAPL')
        tsla = stock_data('TSLA')
        nflx = stock_data('NFLX')
        msft = stock_data('MSFT')

        context = {'AAPL': aapl,
                   'TSLA': tsla,
                   'NFLX': nflx,
                   'MSFT': msft,
                   }
        
        time.sleep(10)
        
        return render(request, 'user_dashboard.html', context)

    
