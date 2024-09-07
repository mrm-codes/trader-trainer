from typing import Any
from django.db import models
from django.contrib.auth.models import User
import yahoo_fin.stock_info as si
import yfinance as yf
import time
from django.db import migrations

import pandas as pd
import plotly.graph_objs as go
from django.http import JsonResponse
#from plotly.offline import plot
import datetime

#User_details
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=10000.00)  # Start with $10,000

    def deposit(self, amount):
        
        self.balance += amount # adding cash to your account 
        self.save()

    def reset_account(self, amount):
        self.balance = 1000.00 #default amouont
        self.save()

    def __str__(self):
        return f"{self.user}'s Account has ${self.balance}"


class Stock(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=100)    


class Portfolio(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, default=str)
    volume = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"You have {self.volume} shares of {self.stock.symbol} bought at {self.price}. Your profit is: {self.profit}"
    

class Transaction(models.Model): 
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, default=1)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, default=str)
    volume = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    transaction_type = models.CharField(max_length=4, choices=(('BUY', 'Buy'), ('SELL', 'Sell')), default=None)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stock.symbol}: {self.volume} shares at {self.price}"


class Trade(models.Model):
    SYMBOL_CHOICES = [
        ('aapl','AAPL'),
        ('tsla', 'TSLA'),
        ('nflx','NFLX'),
        ('msft','MSFT'),
    ]

    ORDER_CHOICES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell')
    ]
    symbol = models.CharField(max_length=6, choices=(SYMBOL_CHOICES), default='AAPL')
    order = models.CharField(max_length=6, choices=(ORDER_CHOICES), default='Buy')
    volume = models.DecimalField(max_digits=10, decimal_places=2, default=0.01)
    price = models.FloatField(default=0)

    
   
 
    

       





 
    



