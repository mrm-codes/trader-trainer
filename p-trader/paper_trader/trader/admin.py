from django.contrib import admin
from .models import User_Account

# Register your models here.
class TraderAdmin(admin.ModelAdmin):
    list_display = ('username', 'balance', 'profit')

admin.site.register(User_Account, TraderAdmin)