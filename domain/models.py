from django.db import models
from common.models import TimeStampedModel

STATUS_CHOICES = [
        ('success', 'Success'),
        ('failure', 'Failure'),
    ]

TYPE_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    ]


class Bank(TimeStampedModel):
    logo = models.ImageField(upload_to='domain/bank/bank_logos/')
    name = models.CharField(max_length=255)
    buy_ling = models.CharField(max_length=255, blank=True, null=True)
    sell_link = models.CharField(max_length=255, blank=True, null=True)
    last_checked = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.bank_name


class Currency(TimeStampedModel):
    country_flag = models.ImageField(
        upload_to='domain/bank/country_flag/', blank=True, null=True)
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255, help_text='Country In Capital')
    short_name = models.CharField(max_length=3,
                                  help_text="Currency shorthand in UPPERCASE")

    def __str__(self):
        return self.short_name


class AggregatorLog(TimeStampedModel):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE,
                             related_name='logs')
    type = models.CharField(max_length=4, choices=TYPE_CHOICES)
    status = models.CharField(max_length=7, choices=STATUS_CHOICES)

    def __str__(self):
        return f'{self.bank.bank_name} - {self.type} - {self.status}'


class Record(TimeStampedModel):
    bank = models.ForeignKey(Bank,
                             on_delete=models.CASCADE, related_name='records')
    currency = models.ForeignKey(Currency,
                                 on_delete=models.CASCADE,
                                 related_name='records')
    type = models.CharField(max_length=4,
                            choices=TYPE_CHOICES)
    value = models.DecimalField(max_digits=10,
                                decimal_places=2)

    def __str__(self):
        return f'{self.bank.bank_name} - {self.currency.short_name} - {self.type}' # noqa
