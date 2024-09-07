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
    
    mytransactions = Transaction.objects.all()
  
    #--------------------------------
    #User account
    user = user_account(request)
    balance = user.balance
    initial_balance = 5000
    min_balance = 0
    transaction_fee = 0.005
    #trade_form = trade(request)
    #Applying functions

    sell_res = sell_stock("AAPL", 0.05, 155.9)

    if request.method == "POST":
        deposit = DepositForm(request.POST)
        reset = ResetForm(request.POST)
    
        #sell = BuyAndSellForm(request.GET)
        if deposit.is_valid():
            amount = deposit.cleaned_data['amount']
            user_balance, created = Account.objects.get_or_create(user=request.user)
            user_balance.balance += amount
            user_balance.save()
            message = messages.success(request, f"${amount} has been added to your balance.")
            return redirect('user_dash')  # Redirect to a profile or dashboard page
        elif reset.is_valid():
            user_balance, created = Account.objects.get_or_create(user=request.user)
            user_balance.balance = initial_balance
            user_balance.save()
       
        
        

    else:
        deposit = DepositForm()
        reset = ResetForm()
        
        
        
    
    
   
    while True:
    #-----------------charting------------------
        aapl = stock_data('AAPL')
        tsla = stock_data('TSLA')
        nflx = stock_data('NFLX')
        msft = stock_data('MSFT')


        #----------------------------------
        aapl_chart = chart('AAPL')
        tsla_chart = chart('TSLA')
        nflx_chart = chart('NFLX')
        msft_chart = chart('MSFT')
        
        time.sleep(10) # 60s interval until fetches another data




        context = {
            'balance': balance,
            'deposit': deposit,
            'reset': reset,
            'sell': sell_res,
          
            
            #'res': res,
            'trans': mytransactions,
            #'trade': trade_form, 
            # stock data
            'AAPL': aapl,
            #'TSLA': tsla,
            #'NFLX': nflx,
            #'MSFT': msft,
            # chart display
            'apple': aapl_chart,
            #'tesla': tsla_chart,
            #'msft': msft_chart,
            #'nflx': nflx_chart,
            #'msg': message
        }

        
        
        return render(request, 'user_dashboard.html', context)
    


    



