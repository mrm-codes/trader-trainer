# Generated by Django 5.1 on 2024-09-10 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trader', '0013_remove_trade_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='symbol',
            field=models.CharField(choices=[('AAPL', 'AAPL'), ('TSLA', 'TSLA'), ('NFLX', 'NFLX'), ('MSFT', 'MSFT'), ('NVDA', 'NVDA'), ('AMZN', 'AMZN'), ('META', 'META'), ('BAC', 'BAC')], default='AAPL', max_length=6),
        ),
    ]
