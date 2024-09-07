from django.contrib import admin
from .models import Account
from django.apps import AppConfig

# Register your models here.
class TraderAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')

admin.site.register(Account, TraderAdmin)


class TradeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trader'

    def ready(self):
        import trader.signals