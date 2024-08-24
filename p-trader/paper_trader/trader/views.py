from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # type: ignore
from django.contrib.auth import login, authenticate # type: ignore
from .forms import RegisterUserForm, LoginUserForm

#Trading requirements
import yahoo_fin.stock_info as si
import yfinance as yf
import time
import requests
from .models import Portfolio, Holdings, Transaction, Overview, TradingCharts
import pandas as pd
import plotly.graph_objs as go
from django.http import JsonResponse
from plotly.offline import plot


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
    def chart(ticker):
        start_period = '2017-01-01'
        end_period = '2024-08-22'
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
    
    aapl_chart = chart('AAPL')
    tsla_chart = chart('TSLA')
    nflx_chart = chart('NFLX')
    msft_chart = chart('MSFT')
           
    while True:

        aapl = Overview.stock_data('AAPL')
        tsla = Overview.stock_data('TSLA')
        nflx = Overview.stock_data('NFLX')
        msft = Overview.stock_data('MSFT')

        #charts
        #aapl_chart_html = my_charts('AAPL')
        #tsla_chart_html = TradingCharts.chart_data('TSLA')
        #nflx_chart_html = TradingCharts.chart_data('NFLX')
        #msft_chart_html = TradingCharts.chart_data('MSFT')

        context = {'AAPL': aapl,
                   'TSLA': tsla,
                   'NFLX': nflx,
                   'MSFT': msft,
                   'apple': aapl_chart,
                   'tesla': tsla_chart,
                   'msft': msft_chart,
                   'nflx': nflx_chart,
                   }
        
        time.sleep(5) # 60s interval until fetches another data
        
        return render(request, 'user_dashboard.html', context)
    

#{'plot': plot_div}
    



