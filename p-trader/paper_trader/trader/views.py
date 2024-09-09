from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth import login, authenticate # type: ignore
from django.contrib import messages
from . forms import RegisterUserForm, LoginUserForm, DepositForm, TransactionForm

#Trading requirements
import yahoo_fin.stock_info as si
import yfinance as yf
import time
import requests
from . models import Account, Transaction
import pandas as pd
import plotly.graph_objs as go
from django.http import JsonResponse
#from plotly.offline import plot
from .functions import *




# Create your views here.

#Base pages/routes
def base(request):
    return render(request, 'base.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def faq(request):
    return render(request, 'faq.html')

#Forms
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


#User dashboard
# Define a Python function

# View function


@login_required
def user_dash(request):
    #Test view------------------------
    myportfolio = Portfolio.objects.all()
    #--------------------------------
    #User account
    user = user_account(request)
    balance = user.balance
    initial_balance = 10000
    min_balance = 0
    transaction_fee = 0.005
    
    

    if request.method == "POST":
        deposit = DepositForm(request.POST, prefix='deposit')
        reset = ResetForm(request.POST, prefix='reset')
        trade_form = TransactionForm(request.POST, prefix='trade_form')
        

        
        
        if deposit.is_valid():
            amount = deposit.cleaned_data['amount']
            
            user_balance, created = Account.objects.get_or_create(user=request.user)
            user_balance.balance += amount
            user_balance.save()
            message = messages.success(request, f"${amount} has been added to your balance.")
            
            return redirect('user_dash')  # Redirect to a profile or dashboard page
  
        elif trade_form.is_valid():
            #current_price = 25
            user_balance, created = Account.objects.get_or_create(user=request.user)
            balance = user_balance.balance
            order = trade_form.cleaned_data['order']
            ticker = trade_form.cleaned_data['symbol']
            volume = trade_form.cleaned_data['volume']
            
           
            
            if order == 'BUY':
                current_price = yf.Ticker(ticker).history(period='1d', interval='1m ')['Close'].iloc[-1]
                price = round(current_price, 2)
                print(f'You are buying {ticker}')
                try:
                    stock = Stock.objects.get(symbol=ticker)
                except Stock.DoesNotExist:
                    if ticker == 'TSLA':
                        stock = Stock.objects.create(symbol=ticker, name='Tesla Inc') 
                        stock.save() # save stock
                    elif ticker == 'NFLX':
                        stock = Stock.objects.create(symbol=ticker, name='Netflix Inc') 
                        stock.save() # save stock
                    elif ticker == 'MSFT':
                        stock = Stock.objects.create(symbol=ticker, name='Microsoft Corporation') 
                        stock.save() # save stock
                    elif ticker == 'NVDA':
                        stock = Stock.objects.create(symbol=ticker, name='NVIDIA Corporation') 
                        stock.save() # save stock
                    elif ticker == 'AMZN':
                        stock = Stock.objects.create(symbol=ticker, name='Amazon Inc') 
                        stock.save() # save stock
                    elif ticker == 'META':
                        stock = Stock.objects.create(symbol=ticker, name='Meta Platforms Inc') 
                        stock.save() # save stock
                    elif ticker == 'BAC':
                        stock = Stock.objects.create(symbol=ticker, name='Bank of America Corp') 
                        stock.save() # save stock
                    else:
                        'Stock does not exist'



                buy_stock(ticker, volume, price)# buy stock
               
                balance = round((Decimal(balance) - (Decimal(price)*Decimal(volume))),2)
                user_balance.save()
                print(f'You bought {volume} shares of {ticker} at ${price}') # resport order
            else:
                print(f'You are selling {ticker}')
                current_price = yf.Ticker(ticker).history(period='1d', interval='1m ')['Close'].iloc[-1]
                price = round(current_price, 2)
                balance = round((Decimal(balance) + (Decimal(price)*Decimal(volume))), 2)
                user_balance.save()
                sell_stock(ticker, volume, price)
                print(f'You sold {volume} shares of {ticker} at ${price}')


        elif reset.is_valid():
            
            user_balance, created = Account.objects.get_or_create(user=request.user)

            portfolio = Portfolio.objects.all()
            portfolio.delete()
                

            user_balance.balance = initial_balance # Reset Balance
            user_balance.save()
            
            
            

           

    else:
        deposit = DepositForm()
        reset = ResetForm()
        trade_form = TransactionForm()
        print('No order')
        

    while True:
    #-----------------stock data------------------
        aapl = stock_data('AAPL')
        tsla = stock_data('TSLA')
        nflx = stock_data('NFLX')
        msft = stock_data('MSFT')
        nvda = stock_data('NVDA')
        amzn = stock_data('AMZN')
        meta = stock_data('META')
        bac = stock_data('BAC')
        #-----------stock chart-----------------------
        aapl_chart = chart('AAPL')
        tsla_chart = chart('TSLA')
        nflx_chart = chart('NFLX')
        msft_chart = chart('MSFT')
        nvda_chart = chart('NVDA')
        amzn_chart = chart('AMZN')
        meta_chart = chart('META')
        bac_chart = chart('BAC')
        
        time.sleep(10) # 10s interval until fetches another data

        


        context = {
            'balance': balance,
            'deposit': deposit,
            'trader': trade_form,     
            'port': myportfolio,
            
            # stock data
            'AAPL': aapl,
            'TSLA': tsla,
            'NFLX': nflx,
            'MSFT': msft,
            'NVDA': nvda,
            'AMZN': amzn,
            'META': meta,
            'BAC': bac,
            #chart display
            'apple': aapl_chart,
            'tesla': tsla_chart,
            'msft': msft_chart,
            'nflx': nflx_chart,
            'nvda':nvda_chart,
            'amzn':amzn_chart,
            'meta': meta_chart,
            'bac': bac_chart,
        
        }

        
        
        return render(request, 'user_dashboard.html', context)
    


@login_required
def transactions(request):
    mytransactions = Transaction.objects.all()
    
    return render(request, 'transaction.html' ,{'trans': mytransactions,})


