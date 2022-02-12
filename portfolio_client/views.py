from django.shortcuts import render
from django.db.models import FloatField, IntegerField, F, Sum, OuterRef, Q, Subquery, Sum
from django.db.models.functions import Coalesce
from django.utils import translation
from .models import Asset
from settings_local import APIS
from urllib.parse import urljoin
import requests

def index(request):
    # Get each asset along with its investment amounts
    asset_list = Asset.objects

    # Get filter and language from query string
    param_filter_name = ''
    translation.activate('en')
    if request.method == 'GET':
        if 'filter' in request.GET:
            param_filter_name = request.GET['filter']
        if 'lang' in request.GET:
            translation.activate(request.GET['lang'])

    if asset_list:
        # Retrieve and summarize values from asset and related tables
        total_dividends = asset_list.annotate(total_dividends=Coalesce(Sum(F('dividend__amount'), output_field=FloatField()), 0.0)).filter(pk=OuterRef('pk'))
        
        # Filter or return all
        if len(param_filter_name) > 0:
            share_amount = asset_list.annotate(share_amount=Coalesce(Sum('assetinvestment__amount', filter=(Q(assetinvestment__filter__name=param_filter_name))), 0)).filter(pk=OuterRef('pk'))
        else:
            share_amount = asset_list.annotate(share_amount=Coalesce(Sum('assetinvestment__amount'), 0)).filter(pk=OuterRef('pk'))

        total_paid_value = asset_list.annotate(total_paid_value=Coalesce(Sum(F('assetinvestment__amount') * F('assetinvestment__paid_price'), output_field=FloatField()), 0.0)).filter(pk=OuterRef('pk'))
        total_fees = asset_list.annotate(total_fees=Coalesce(Sum(F('assetinvestment__total_fees') * -1.0, output_field=FloatField()), 0.0)).filter(pk=OuterRef('pk'))        
        
        asset_list = asset_list.annotate(
            total_dividends=Coalesce(Subquery(total_dividends.values('total_dividends')), 0, output_field=FloatField()),
            share_amount=Coalesce(Subquery(share_amount.values('share_amount')), 0, output_field=IntegerField()),
            total_paid_value=Coalesce(Subquery(total_paid_value.values('total_paid_value')), 0, output_field=FloatField()),
            total_fees=Coalesce(Subquery(total_fees.values('total_fees')), 0, output_field=FloatField()),
        ).filter(share_amount__gt=0)

        # Grid data
        result =  {
            'asset_list': [],
            'total_stock_value': 0.0,
            'total_paid_value':  0.0,
            'total_change': 0.0,
            'total_fees': 0.0,
            'total_dividends': 0.0,
            'total_value': 0.0,
            'total_profits': 0.0
        }
        
        # Retrieving all symbols first because API does not support retrieval by symbol
        apis = load_info_lists()
        if apis != None and len(apis) > 0:
            # Get current price for each asset, and total price
            for asset in asset_list:
                # Retrieve price for each asset
                for api in apis:                    
                    info = get_info(api, asset.symbol)
                    if info is not None:
                        # Calculate other data based on API price
                        asset.price = convert_to_money(info[api['field_price']])
                        asset.name = info[api['field_name']]
                        asset.total_stock_value = asset.share_amount * asset.price
                        result['total_paid_value'] += asset.total_paid_value
                        result['total_stock_value'] += asset.total_stock_value
                        result['total_fees'] += asset.total_fees
                        result['total_dividends'] += asset.total_dividends
                        break
        
                # Remaining calculated data may not rely on API
                if hasattr(asset, 'price'):
                    asset.total_value = asset.total_stock_value + asset.total_dividends
                    asset.total_profits = asset.total_value + asset.total_fees - asset.total_paid_value 
                    result['total_value'] += asset.total_value
                    result['total_profits'] += asset.total_profits

        # Calculate portfolio percentage for each asset
        for asset in asset_list:
            if hasattr(asset, 'price'):
                asset.total_change = get_total_change(asset.total_paid_value, asset.total_stock_value)
                asset.percentage = get_percentage(asset.price, asset.share_amount, result['total_stock_value'])
                result['asset_list'].append(asset)
    
    return render(request, 'portfolio_client/index.html', result)

def load_info_lists():
    # Get data from multiple API endpoints
    for api in APIS:
        # Prepare request
        body = requests.request(api['request_type'], urljoin(api['root'], api['status']), data=api['params'])

        # Handle response
        if body.status_code == 200:
            if api['type'] == 'json':
                api['data'] = body.json()

    # Get only APIs where data retrieved
    return list(filter(lambda api: api['data'] is not None and len(api['data']) > 0, APIS))

def get_info(api, symbol):
    try:
        return next(filter(lambda symbol_data: symbol_data[api['field_symbol']] == symbol, api['data']))
    except:
        return None

def get_percentage(price, amount, total_value):
    if total_value == 0:
        return 0    
    return price * amount / total_value * 100

def get_total_change(old, new):
    if (new == 0):
        return 0
    return (new - old) / old * 100

def convert_to_money(price):
    if isinstance(price, str):
        price = price.replace(',', '.')
    return float(price)
