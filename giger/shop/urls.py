from django.urls import path
from shop.views import *

urlpatterns = [
    path('', homePage, name='home'),

    path('product/<slug:product_slug>', productPage, name='product'),
    path('category/<slug:category_slug>', categoryPage, name='category'),
    path('search', searchPage, name='search'),
    path('wishlist', wishlistPage, name='wishlist'),
    path('cart', cartPage, name='cart'),
    path('checkout', checkOutPage, name='checkout'),
    path('checkout/success', checkOutSuccessPage, name='checkout_success'),

    path('api/getProduct/<int:product_id>', getProductApi),
]