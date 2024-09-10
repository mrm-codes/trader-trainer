from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth import login, authenticate # type: ignore
from .forms import RegisterUserForm, LoginUserForm, DepositForm, TransactionForm, ResetForm
#Trading requirements
import time
from .models import Account, Transaction
from .functions import *

#Static pages/routes
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

#reset account
@login_required
def reset_account(request):
    user_balance, created = Account.objects.get_or_create(user=request.user)
    
    
    if request.method ==  'POST':
        reset = ResetForm(request.POST, prefix='reset_account')
        if reset.is_valid():
            portfolio = Portfolio.objects.all().delete()
            initial_balance = 100000 # $100,000.00
            user_balance.balance = initial_balance # Reset Balance
            user_balance.save()
            reset = ResetForm()
            redirect('/user_dash')
            print('Account reset')
        else:
            reset = ResetForm()
            print('Account not reset')
    return render(request, 'user_dashboard.html', {'reset': reset,})

#User dashboard
@login_required
def user_dash(request):

    #User account
    user_balance, created = Account.objects.get_or_create(user=request.user)
    balance = user_balance.balance

    #updating portfolio
    myportfolio = Portfolio.objects.all()
    for asset in myportfolio:
        asset_symbol = asset.stock.symbol
        asset_price = asset.price
        asset_volume = asset.volume
        asset_current_price = live_price(asset_symbol)
        asset_profit = (Decimal(asset_current_price) - Decimal(asset_price))*Decimal(asset_volume)
        new_profit = round(asset_profit,2)
        asset.profit = new_profit 
        asset.save()
        
    
    if request.method == "POST":
        deposit = DepositForm(request.POST, prefix='deposit')
        trade_form = TransactionForm(request.POST, prefix='trade_form')

        if deposit.is_valid():
            amount = deposit.cleaned_data['amount']
            balance += amount
            user_balance.save()
            deposit = DepositForm()
            print(f'You added ${amount}')
       
            #return redirect('user_dash')  # Redirect to a profile or dashboard page
  
        elif trade_form.is_valid():

            order = trade_form.cleaned_data['order']
            ticker = trade_form.cleaned_data['symbol']
            volume = trade_form.cleaned_data['volume']
            
            if order == 'BUY':
                price = live_price(ticker)
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
                trade_form = TransactionForm() # clearing the form
                print(f'You bought {volume} shares of {ticker} at ${price}') # resport order
            else:
                print(f'You are selling {ticker}')
                price = round(live_price(ticker), 2)
                
                sell_stock(ticker, volume, price)
                
                balance = round((Decimal(balance) + (Decimal(price)*Decimal(volume))), 2)
                user_balance.save()
                trade_form = TransactionForm()
                print(f'You sold {volume} shares of {ticker} at ${price}')


    else:
        deposit = DepositForm()
        trade_form = TransactionForm()
        print('No order')
        
 
    while True:
    #information    
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


