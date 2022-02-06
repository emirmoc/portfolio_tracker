from django.contrib import admin

from .models import Asset, AssetInvestment, Filter, Dividend

admin.site.register(Asset)
admin.site.register(AssetInvestment)
admin.site.register(Dividend)
admin.site.register(Filter)