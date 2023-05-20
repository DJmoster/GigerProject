from django.urls import path
from shop.views import *

urlpatterns = [
    path('', homePage, name='home'),
    path('product/<slug:product_slug>', productPage, name='product')
]