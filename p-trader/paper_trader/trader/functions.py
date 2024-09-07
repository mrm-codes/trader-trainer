from decimal import Decimal
from django.db import transaction
from django.apps import apps
import yahoo_fin.stock_info
from .models import Account, Stock, Portfolio, Transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect # type: ignore
from django.http import JsonResponse
from django.contrib import messages
from .forms import DepositForm, ResetForm, TransactionForm

import yahoo_fin
import yfinance as yf
import datetime
import plotly.graph_objs as go
from django.http import JsonResponse


#------------------------------------
#Adding stocks to DB
'''stock_info = Stock.objects.create(symbol='AAPL', name='Apple')
stock_info.save()'''


#-----------------------------------

'''
Account
deposit, reset
----------------------------

Trading functions
buy, sell, close, 

Data Overview
Stock(name, symbol, bid, ask, daily_change, price_per_share)

Data Visualzation
Stock(chart, chart name, current price)

Portfolio
Time, symbol, transation_type, volume, open_price, current_price, profit

Transaction
Time, symbol, transation_type, volume, open_price, close_price, profit
'''
#---Account functions done with the model------#
#BUY FUNCTION
# When you buy your balance does't change, creates a portfolio, where price is open_price and profit = (1-transaction_fee)*price*volume

#checkin item in DB
'''apple = Transaction.objects.get(id=1).portfolio.stock.symbol  
print(apple)'''

#checking DB
''']
acc = apps.get_model('trader', 'Stock')
field_name_1 = [field.name for field in Stock._meta.get_fields()]
print(field_name_1)
bcc = apps.get_model('trader', 'Portfolio')
field_name_2 = [field.name for field in Portfolio._meta.get_fields()]

ccc = apps.get_model('trader', 'Transaction')
field_nam_3 = [field.name for field in Transaction._meta.get_fields()]
'''

@login_required
#User account
def user_account(request):
    account = request.user.account
    return account

#Trading info
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
           
            #getting the current bid
            on_price = stock.info.get('bid', 'No data available')
            bid = round(on_price, 2)


            #Getting the current ask
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
                'daily_change': 'daily_change',
                }

def chart(ticker):
    start_period = '2017-01-01'
    today = '2024-08-30'
    end_period = today
    interval = '1d'



    df = yf.download(ticker, start=start_period, end=end_period, interval=interval)

    #chartting
        # Create a mountain chart (area chart)
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                                        open=df['Open'],
                                        high=df['High'],
                                        low=df['Low'],
                                        close=df['Close'])])

    fig.update_layout(
        title=f'{ticker} Stock Price',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        height=600,  # Set height
        width=1200,  # Set width
        autosize=True,
        
        margin=dict(l=20, r=20, t=40, b=40))

    ticker_chart = fig.to_html(full_html=False)
    return ticker_chart


#Trading operations 
def buy_stock(ticker, volume, price):
    try:
        stock = Stock.objects.get(symbol = ticker)
    except Stock.DoesNotExist:
        return 'Stock symbol not found'

    portfolio, created = Portfolio.objects.get_or_create(stock=stock, defaults={'volume': 0, 'price': 0})

    with transaction.atomic():
        total_cost = Decimal(volume*price)
        total_volume = Decimal(portfolio.volume) + Decimal(volume)
        avg_price = (Decimal(portfolio.volume*portfolio.price) + Decimal(total_cost))/Decimal(total_volume)

        portfolio.volume = total_volume
        portfolio.price = avg_price
        portfolio.save()

        Transaction.objects.create(
            portfolio=portfolio,
            stock=stock,
            volume=volume,
            price=price,
            transaction_type = 'BUY',
            
        )
    return f'Successfully bought {volume} shares of {ticker} at ${price}.'


def sell_stock(ticker, volume, price):
    try:
        stock = Stock.objects.get(symbol=ticker)
    except Stock.DoesNotExist:
        return "Stock symbol not found."
    
    try:
        portfolio = Portfolio.objects.get(stock=stock)
    except Portfolio.DoesNotExist:
        return "You don't own this stock."
    
    if portfolio.volume < volume:
            return "Not enough stock to sell."

        
    with transaction.atomic():
        total_revenue = Decimal(volume)*Decimal(price)
        new_volume = Decimal(portfolio.volume) - Decimal(volume)

        if new_volume == 0:
            portfolio.delete()
            message = f'You sold all {ticker} shares'
            return message
        else:
            portfolio.volume = new_volume
            portfolio.save()

        Transaction.objects.create(
            portfolio = portfolio,
            stock =stock,
            transaction_type = 'SELL',
            volume = volume,
            price = price
        )
    
    return f"Successfully sold {volume} shares of {ticker} at ${price}."






        
    