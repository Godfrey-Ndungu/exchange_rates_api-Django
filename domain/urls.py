from django.urls import path
from .views import BankCurrencyListView

urlpatterns = [
    path('currencies', BankCurrencyListView.as_view(), name='bank_list'),
]
