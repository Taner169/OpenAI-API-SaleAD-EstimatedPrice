from django.urls import path
from .views import sale_ad_view

urlpatterns = [
    path('', sale_ad_view, name='sale_ad_view'),
]
