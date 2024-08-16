from django.db import models
import datetime

#User_details
class User_Details(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=250)


#Portfolio
class Portfolio(models.Model):
    name = models.CharField(max_length=50, default='')
    symbol = models.CharField(max_length=10, default='')
    volume = models.FloatField(default=0)
    price = models.FloatField(default=0)
    profit_in_number = models.FloatField(verbose_name='profit', default=0)
    profit_in_percentage = models.FloatField(verbose_name='profit (%)', default=0)
    date = models.DateField(default=datetime.date.today)



#User_account
class User_Account(User_Details):
    username = User_Details.first_name
    balance = models.FloatField(default=1000)
    profit = Portfolio.profit_in_percentage