from django.shortcuts import get_object_or_404, render

from shop.models import Products, ProductImages, ProductReviews

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

    if request.method == 'POST':
        ProductReviews.objects.create(
            product_id  = product,
            name        = request.POST.get('name'),
            email       = request.POST.get('email'),
            description = request.POST.get('review'),
            rate        = request.POST.get('stars'),
        )

    images  = ProductImages.objects.filter(product_id=product.pk)
    reviews = ProductReviews.objects.filter(product_id=product.pk)

    reviews_count = []
    for i in range(1,6):
        reviews_count.append(len(reviews.filter(rate=i)))

    reviews_count.reverse()

    reviews_sum = len(reviews)
    reviews_avg = round((reviews_count[0] * 5 + 
                   reviews_count[1] * 4 + 
                   reviews_count[2] * 3 + 
                   reviews_count[3] * 2 + 
                   reviews_count[4] * 1) / reviews_sum, 1)

    context = {
        'page_title': 'Giger | ' + product.name,
        'product_object': product,
        'product_images': images,
        'product_reviews': reviews,
        'product_reviews_count': reviews_count,
        'product_reviews_sum': reviews_sum,
        'product_reviews_avg': reviews_avg,
    }

    return render(request, 'shop/product.html', context=context)