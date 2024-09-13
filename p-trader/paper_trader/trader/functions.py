from decimal import Decimal
from django.db import transaction
from django.apps import apps

from .models import Account, Stock, Portfolio, Transaction
from django.contrib.auth.decorators import login_required
import yfinance as yf

import datetime
import plotly.graph_objs as go



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
        current_price = stock.info.get('currentPrice')
        price = round(current_price, 2)
        if not data_history.empty:
            # Get the opening price (first price of the day)
            opening_price = data_history['Open'][0]
           
            #getting the current bid
            on_price = stock.info.get('bid', 'No data available')
            bid = round(on_price, 2)


            #Getting the current ask
            off_price = stock.info.get('ask', 'No data available')
            ask = round(off_price, 2)


            # Calculate daily change percentage
            daily_change_percentage = ((price - opening_price) / opening_price) * 100
            daily_change = round(daily_change_percentage, 2)
        else:
            print(message)
       
        return  {'ticker': ticker,
                'bid': bid,
                'ask': ask,
                'price': price,
                'daily_change': daily_change,
                }

def chart(ticker):
    start_period = '2017-01-01'
    today = datetime.date.today()
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
        width=1100,  # Set width
        autosize=True,
        
        margin=dict(l=20, r=20, t=40, b=40))

    ticker_chart = fig.to_html(full_html=False)
    return ticker_chart

#current price

def live_price(ticker):
    stock_price = yf.Ticker(ticker).info.get('currentPrice')
    price = round(stock_price, 2)
    return price
#Trading operations 
def buy_stock(ticker, volume, price):
    price = live_price(ticker)
    try:
        stock = Stock.objects.get(symbol = ticker)
    except Stock.DoesNotExist:
        return 'Stock symbol not found'

    portfolio, created = Portfolio.objects.get_or_create(stock=stock, defaults={'volume': 0, 'price': 0})

    with transaction.atomic():
        total_cost = Decimal(volume)*Decimal(price)
        total_volume = Decimal(portfolio.volume) + Decimal(volume)
        avg_price = (Decimal(portfolio.volume*portfolio.price) + Decimal(total_cost))/Decimal(total_volume)

        

        initial_profit = (Decimal(price) - Decimal(portfolio.price))*Decimal(portfolio.volume)
          
          

        portfolio.volume = total_volume
        portfolio.price = avg_price
        portfolio.profit = initial_profit
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
    price = live_price(ticker)
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
        
        if volume < portfolio.volume:
            partial_profit = round(((Decimal(portfolio.price) - Decimal(price))*Decimal(volume)),2)
            portfolio.profit = partial_profit
            portfolio.save()
        if volume == portfolio.volume:
            total_profit = round(((Decimal(portfolio.price) - Decimal(price))*Decimal(portfolio.volume)),2)
            portfolio.profit = total_profit
            portfolio.save()

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


stocks_list = {
    'AAPL': 'Apple Inc.',
    'TSLA': 'Tesla Inc',
    'NFLX': 'Netflix Inc', 
    'MSFT': 'Microsoft Corporation', 
    'NVDA': 'NVIDIA Corporation', 
    'AMZN': 'Amazon Inc', 
    'META': 'Meta Platforms Inc', 
    'BAC': 'Bank of America Corp',
}



