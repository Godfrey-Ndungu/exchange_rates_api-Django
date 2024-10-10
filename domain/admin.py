from django.contrib import admin
from .models import Bank, Currency, AggregatorLog, Record
from unfold.admin import ModelAdmin


admin.site.site_header = 'Exchange Rates'
admin.site.site_title = "Exchange Rates"
admin.site.index_title = "Exchange Rates"


@admin.register(Bank)
class BankAdmin(ModelAdmin):
    list_display = ('name', 'last_checked')
    search_fields = ('name',)
    list_filter = ('last_checked',)


@admin.register(Currency)
class CurrencyAdmin(ModelAdmin):
    list_display = ('name', 'country', 'short_name')
    search_fields = ('name', 'short_name', 'country')
    list_filter = ('country',)


@admin.register(AggregatorLog)
class AggregatorLogAdmin(ModelAdmin):
    list_display = ('bank', 'type', 'status', 'created_at')
    search_fields = ('bank__name', 'type', 'status')
    list_filter = ('status', 'type', 'created_at')


@admin.register(Record)
class RecordAdmin(ModelAdmin):
    list_display = ('bank', 'currency', 'type', 'value', 'created_at')
    search_fields = ('bank__name', 'currency__short_name', 'type')
    list_filter = ('type', 'bank', 'currency', 'created_at')
