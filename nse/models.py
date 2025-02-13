from django.db import models

class QuoteData(models.Model):
    date = models.DateField()
    expiry_date = models.DateField()
    option_type = models.CharField(max_length=10)
    strike_price = models.FloatField(null=True, blank=True)
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    close_price = models.FloatField()
    last_price = models.FloatField()
    settle_price = models.FloatField()
    volume = models.BigIntegerField()
    value = models.CharField(max_length=255)
    premium_value = models.CharField(max_length=255)
    open_interest = models.BigIntegerField()
    change_in_oi = models.BigIntegerField()

    def __str__(self):
        return f"{self.date} - {self.expiry_date} - {self.option_type}"
