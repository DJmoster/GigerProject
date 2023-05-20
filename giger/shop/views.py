from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from shop.models import Products, ProductImages

def error404Page(request, exception):
    context = {
        'page_title': f'Giger | 404',
    }
    return render(request, 'shop/error.html', context=context)

def homePage(request):
    context = {
        'page_title': 'Giger | Home',
    }
    return render(request, 'shop/home.html', context=context)

def productPage(request, product_slug):
    product = get_object_or_404(Products, url_slug=product_slug)
    images  = ProductImages.objects.filter(product_id=product.pk)

    context = {
        'page_title': 'Giger | ' + product.name,
        'product_object': product,
        'product_images': images,
    }

    return render(request, 'shop/product.html', context=context)