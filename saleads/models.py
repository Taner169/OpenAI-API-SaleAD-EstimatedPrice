from django.db import models

class SaleAd(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='saleads/')
    description = models.TextField(blank=True)
    price_estimate = models.TextField(blank=True) 
