from django.db import models

# Create your models here.

max_money_digits = 9
money_decimal_places = 2

class Filter(models.Model):
    name = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return self.name

class Asset(models.Model):
    symbol = models.CharField(max_length=20, unique=True)
    link_info = models.CharField(max_length=5000, default=None, blank=True, null=True)
    def __str__(self):
        return self.symbol

class AssetInvestment(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    filter = models.ForeignKey(Filter, blank=True, null=True, on_delete=models.SET_NULL)
    amount = models.IntegerField()
    paid_price = models.DecimalField(max_digits=max_money_digits, decimal_places=money_decimal_places)
    total_fees = models.DecimalField(max_digits=max_money_digits, decimal_places=money_decimal_places, default=0.0)
    date = models.DateTimeField('date')

class Dividend(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=max_money_digits, decimal_places=money_decimal_places, default=0.0)
    date = models.DateTimeField('date')