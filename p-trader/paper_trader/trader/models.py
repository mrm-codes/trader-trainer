from typing import Any
from django.db import models
from django.contrib.auth.models import User
import yahoo_fin.stock_info as si
import yfinance as yf
import time
import requests

import datetime

#User_details
class Portfolio(models.Model):
    user = User.username
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=10000.00)  # Start with $10,000

    def __str__(self):
        return f"{self.user}'s Portfolio"

class Holdings(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.symbol}: {self.quantity} shares"
    

class Transaction(models.Model):
    symbol = models.CharField(max_length=10, default='')
    volume = models.FloatField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.symbol}: {self.quantity} shares at {self.price}"


class Overview(models.Model):
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    #fetching bid and ask
    ticker = 'TSLA'
    

    #fetching prices
    def live_price(ticker):
        stock = yf.Ticker(ticker)
        data_history = stock.history(period='1d', interval='1m ')

        if not data_history.empty:
            return data_history['Close'].iloc[-1]
        else:
            return None
        
    def daily_change(ticker):
       
        data_history = yf.Ticker(ticker).history(period='1d', interval='1m')
        
         # Check if there's data available
        if not data_history.empty:
            # Get the opening price (first price of the day)
            opening_price = data_history['Open'][0]
            
            # Get the current or last close price (latest price of the day)
            current_price = data_history['Close'].iloc[-1]

            # Calculate daily change percentage
            daily_change_percentage = ((current_price - opening_price) / opening_price) * 100

            return  round(daily_change_percentage, 2)
        else:
            return None
    
    while True:
        # Fetch the current price
        price = round(live_price(ticker), 2)
        daily_change_percent = daily_change(ticker)

        #on_price = yf.Ticker(ticker).fast_info.last_price
        on_price = yf.Ticker(ticker).info.get('bid', 'No data available')
        bid = round(on_price, 2)

        #off_price = yf.Ticker(ticker).fast_info.previous_close
        off_price = yf.Ticker(ticker).info.get('ask', 'No data available')
        ask = round(off_price, 2)
        
        if price is not None:
            print(f"Current price of {ticker}: ${price}")
            print(f"{ticker} => Ask: ${ask}, Bid: ${bid}, Daily change: {daily_change_percent}%" )
        else:
            print(f"Failed to fetch data for {ticker}.")
        
        # Wait for 30 seconds before fetchingticker
        time.sleep(30)



