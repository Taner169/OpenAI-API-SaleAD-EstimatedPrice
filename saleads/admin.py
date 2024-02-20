from django.contrib import admin
from .models import SaleAd

class SaleAdAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'description') 
admin.site.register(SaleAd, SaleAdAdmin)
