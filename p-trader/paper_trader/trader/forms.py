from typing import Any, Mapping
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms.renderers import BaseRenderer
from django.forms.utils import ErrorList
from .models import Account, Portfolio, Transaction, Trade
from django import forms

class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs).__init__
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

class LoginUserForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')
    
    def __init__(self, *args: Any, **kwargs):
        super(AuthenticationForm, self).__init__( *args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'

class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Account
        fields = ['amount']
    
    def __init__(self, *args, **kwargs):
        intance = kwargs.get('instance')
        super(DepositForm, self).__init__(*args, kwargs)


class ResetForm(forms.Form):
    class Meta:
        model = Account
    
    def __init__(self, *args, **kwargs):
        intance = kwargs.get('instance')
        super(ResetForm, self).__init__(*args, kwargs)
    
class TransactionForm(forms.ModelForm):
    
    class Meta:
        model = Trade
        fields = ['symbol', 'order', 'volume', 'price']

    def __init__(self, *args, **kwargs):
        intance = kwargs.get('instance')
        super(TransactionForm, self).__init__(*args, kwargs)
        
    