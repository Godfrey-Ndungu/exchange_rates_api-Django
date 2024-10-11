from rest_framework.views import APIView
from django.http import JsonResponse
from .models import Bank, Record, Currency


class BankCurrencyListView(APIView):
    """
        Bank Currency API Documentation
        ===============================

        This documentation provides details about the API to retrieve
        bank information along with their associated currencies, buy and sell 
        records. This API delivers data in JSON format and is built using
          Django Rest Framework (DRF).

        Overview
        --------

        The API retrieves a list of banks, each containing a list of
          currencies and their respective buy and sell rates. Each record
            provides details about the bank, currency, and transaction rates,
              including the latest buy and sell rates.

        Endpoint
        --------

        .. http:get:: /api/bank-currency/

        Returns a list of banks with their currencies, buy and sell records.

        Response Format
        ---------------

        The response consists of a list of banks. Each bank contains the
        following information:

        - **id**: Unique identifier for the bank
        - **name**: Name of the bank
        - **logo**: URL to the bank's logo
        - **currencies**: List of currencies associated with the bank
            - **id**: Unique identifier for the currency
            - **name**: Full name of the currency
            - **short_name**: Abbreviation of the currency (e.g., USD, EUR)
            - **country_flag**: URL to the country flag image
            - **buy**: The buy rate for the currency (if available)
                - **id**: Unique identifier for the buy record
                - **value**: Buy value (in decimal format)
            - **sell**: The sell rate for the currency (if available)
                - **id**: Unique identifier for the sell record
                - **value**: Sell value (in decimal format)

        Example JSON Response
        ---------------------

        Below is an example response from the API:

        .. code-block:: json

            [
                {
                    "id": 1,
                    "name": "Bank A",
                    "logo": "https://example.com/path/to/bank-logo.jpg",
                    "currencies": [
                        {
                            "id": 1,
                            "name": "US Dollar",
                            "short_name": "USD",
                            "country_flag": /path/to/flag.jpg",
                            "buy": {
                                "id": 101,
                                "value": "9675.68"
                            },
                            "sell": {
                                "id": 102,
                                "value": "6432.12"
                            }
                        },
                        {
                            "id": 2,
                            "name": "Euro",
                            "short_name": "EUR",
                            "country_flag": "/path/to/flag.jpg",
                            "buy": {
                                "id": 103,
                                "value": "8700.50"
                            },
                            "sell": {
                                "id": 104,
                                "value": "8650.00"
                            }
                        }
                    ]
                },
                {
                    "id": 2,
                    "name": "Bank B",
                    "logo": "https://example.com/path/to/bank-logo2.jpg",
                    "currencies": [
                        {
                            "id": 3,
                            "name": "Kenyan Shilling",
                            "short_name": "KES",
                            "country_flag": "path/to/flag.jpg",
                            "buy": {
                                "id": 201,
                                "value": "1.10"
                            },
                            "sell": {
                                "id": 202,
                                "value": "1.00"
                            }
                        }
                    ]
                }
            ]

        How to Use
        ----------

        1. Send a GET request to the `/api/bank-currency/` endpoint.
        2. The API will return a list of banks, with each bank
          containing its currencies and the associated buy and sell rates.

        Dependencies
        ------------

        This API relies on the following models:

        - **Bank**: Represents a financial institution.
        - **Currency**: Represents a currency with a country flag.
        - **Record**: Represents a transaction record for buy or sell actions.
        - **AggregatorLog**: Logs for tracking the status of transactions.

        Example Python Code for API Request
        -----------------------------------

        .. code-block:: python

            import requests

            url = 'https://example.com/api/bank-currency/'
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                for bank in data:
                    print(bank['name'], bank['currencies'])
            else:
                print('Error:', response.status_code)

    """
    def get(self, request, *args, **kwargs):
        banks = Bank.objects.all()
        response_data = []

        for bank in banks:
            bank_data = {
                'id': bank.id,
                'name': bank.name,
                'logo': bank.logo.url if bank.logo else None,
                'currencies': []
            }

            currencies = Currency.objects.filter(records__bank=bank).distinct()

            for currency in currencies:
                currency_data = {
                    'id': currency.id,
                    'name': currency.name,
                    'short_name': currency.short_name,
                    'country_flag': currency.country_flag.url if currency.country_flag else None, # noqa
                    'buy': None,
                    'sell': None
                }

                # Get buy and sell records for the currency
                buy_record = Record.objects.filter(bank=bank,
                                                   currency=currency,
                                                   type='buy').last()
                sell_record = Record.objects.filter(bank=bank,
                                                    currency=currency,
                                                    type='sell').last()

                if buy_record:
                    currency_data['buy'] = {
                        'id': buy_record.id,
                        'value': str(buy_record.value)
                    }

                if sell_record:
                    currency_data['sell'] = {
                        'id': sell_record.id,
                        'value': str(sell_record.value)
                    }

                bank_data['currencies'].append(currency_data)

            response_data.append(bank_data)

        return JsonResponse(response_data, safe=False)
