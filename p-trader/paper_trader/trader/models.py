from typing import Any
from django.db import models
from django.contrib.auth.models import User
import yahoo_fin.stock_info as si
import yfinance as yf
import time

import pandas as pd
import plotly.graph_objs as go
from django.http import JsonResponse
from plotly.offline import plot

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
                'daily_change': 'daily_change',
                }


    
    
    
    
   
 
    


       





 
    



