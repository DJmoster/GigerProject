from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator

import json

from shop.forms import OrderForm, ReviewForm
from shop.models import Products, ProductImages, ProductReviews, Categories, Customers, Orders, OrderItems

APP_NAME = 'Giger'

def error404Page(request, exception):
    categories = Categories.objects.filter(is_active=True)

    context = {
        'page_title': f'{APP_NAME} | 404',
        'page_categories': categories,
    }
    return render(request, 'shop/error.html', context=context)

def homePage(request):
    categories = Categories.objects.filter(is_active=True)

    context = {
        'page_title': f'{APP_NAME} | Home',
        'page_categories': categories,
    }
    return render(request, 'shop/home.html', context=context)

def productPage(request, product_slug):
    categories = Categories.objects.filter(is_active=True)
    product = get_object_or_404(
        Products, 
        url_slug=product_slug, 
        is_active=True, 
        category_id__is_active=True
    )

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            ProductReviews.objects.create(
                product_id  = product,
                name        = request.POST.get('name'),
                email       = request.POST.get('email'),
                description = request.POST.get('review'),
                rate        = request.POST.get('stars'),
            )

    images  = ProductImages.objects.filter(product_id=product.pk)
    reviews = ProductReviews.objects.filter(product_id=product.pk)

    context = {
        'page_title': f'{APP_NAME} | ' + product.name,
        'page_categories': categories,
        'product_object': product,
        'product_images': images,
        'product_reviews': reviews.order_by('-creation_date'),
        'product_reviews_len': len(reviews),
    }

    return render(request, 'shop/product.html', context=context)

def categoryPage(request, category_slug):
    categories = Categories.objects.filter(is_active=True)
    category = get_object_or_404(
        Categories, 
        url_slug=category_slug, 
        is_active=True
    )
    products = Products.objects.filter(
        category_id=category.pk, 
        is_active=True
    )

    # Перевірка поля sortBy   
    try:
        sort_method = int(request.GET.get('sortBy'))
    except TypeError:
        sort_method = 1
    except ValueError:
        return redirect(category.get_absolute_url())
    
    if sort_method < 1 and sort_method > 5:
        return redirect(category.get_absolute_url())
    
    # Вибір методу сортування обєктів
    if sort_method == 2:
        products = products.order_by('-creation_date')
    elif sort_method == 3:
        products = products.order_by('creation_date')
    elif sort_method == 4:
        products = products.order_by('price')
    elif sort_method == 5:
        products = products.order_by('-price')


    # Перевірка поля show
    try:
        products_per_page = int(request.GET.get('show'))
    except TypeError:
        products_per_page = 20
    except ValueError:
        return redirect(category.get_absolute_url())
    
    if products_per_page < 0:
        return redirect(category.get_absolute_url())
    if products_per_page == 0:
        products_per_page = len(products)

    # Розбиття обєктів на сторінки
    paginate = Paginator(products, products_per_page)

    # Перевірка поля page   
    try:
        page = int(request.GET.get('page'))
    except TypeError:
        page = 1
    except ValueError:
        return redirect(category.get_absolute_url())

    if page > paginate.num_pages or page < 1:
        return redirect(category.get_absolute_url())


    context = {
        'page_title': f'{APP_NAME} | {category.name}',
        'page_categories': categories,
        'category_object': category,
        'category_products': paginate.page(page),
        'category_products_count': len(products),
        'paginator': paginate,
        'paginator_page': page,
        'paginator_start': products_per_page * (page - 1) + 1,
        'paginator_end': products_per_page * page,
    }

    return render(request, 'shop/category.html', context=context)

def searchPage(request):
    categories = Categories.objects.filter(is_active=True)
    # Перевірка поля s 
    try:
        search_text = str(request.GET.get('s'))
    except TypeError:
        return redirect('home')
    except ValueError:
        return redirect('home')
    
    if len(search_text) > 255 or search_text == 'None':
        return redirect('home')

    products = Products.objects.filter(
        name__contains=search_text,
        is_active=True,
    )

    print(products)

    # Розбиття обєктів на сторінки
    products_per_page = 20
    paginate = Paginator(products, products_per_page)

    # Перевірка поля page   
    try:
        page = int(request.GET.get('page'))
    except TypeError:
        page = 1
    except ValueError:
        return redirect('home')

    if page > paginate.num_pages or page < 1:
        return redirect('home')

    context = {
        'page_title': f'{APP_NAME} | Пошук',
        'page_categories': categories,
        'search_text': search_text,
        'search_products': paginate.page(page),
        'search_products_count': len(products),
        'paginator': paginate,
        'paginator_page': page,
        'paginator_start': products_per_page * (page - 1) + 1,
        'paginator_end': products_per_page * page,
    }

    return render(request, 'shop/search.html', context=context)

def getProductApi(request, product_id):
    product = get_object_or_404(
        Products,
        pk=product_id,
        is_active=True, 
        category_id__is_active=True
    )

    response = {
        'product': {
            'id': product.pk,
            'slug': product.url_slug,
            'name': product.name,
            'price': product.price,
            'image': product.get_product_image.image.url,
            'availability': product.availability,
        }
    }

    return JsonResponse(response)

def wishlistPage(request):
    categories = Categories.objects.filter(is_active=True)

    context = {
        'page_title': f'{APP_NAME} | Список бажаного',
        'page_categories': categories,
    }
    return render(request, 'shop/wishlist.html', context=context)

def cartPage(request):
    categories = Categories.objects.filter(is_active=True)

    context = {
        'page_title': f'{APP_NAME} | Корзина',
        'page_categories': categories,
    }

    return render(request, 'shop/cart.html', context=context)

def checkOutPage(request):
    categories = Categories.objects.filter(is_active=True)

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            try:
                order_items = json.loads(request.POST.get('products'))
            except ValueError:
                return HttpResponse(status=500)

            customer = Customers(
                name    = request.POST.get('name'),
                surname = request.POST.get('surname'),
                address = f"{request.POST.get('city')} {request.POST.get('street')} {request.POST.get('streetNumber')}",
                phone   = request.POST.get('phoneNubmer')
            )
            customer.save()

            order = Orders(
                customer_id = customer,
                notes       = '',
                shipping_method = request.POST.get('shipping_method'),
            )
            order.save()

            for item in order_items:
                product     = Products.objects.get(pk=item.get('id'))
                item_model  = OrderItems(
                    product_id   = product,
                    order_id     = order,
                    name         = product.name,
                    buying_price = product.price,
                    count        = item.get('count')
                )
                item_model.save()
            return redirect('checkout_success')

    context = {
        'page_title': f'{APP_NAME} | Оформити замовлення',
        'page_categories': categories,
        'shipping_methods': (
            ('Доставка Нова пошта', 'Замовлення відправляється через нову пошту оплата при отриманні посилки.', 'novaPoshta'),
            ('Доставка Укр пошта', 'Замовлення відправляється через укр пошту оплата при отриманні посилки.', 'urkPoshta'),
            ('Самовивіз', 'Отримуєте замовлення в одному з нащих магазинів.', 'selfPickUp'),
        ),
    }

    return render(request, 'shop/checkout.html', context=context)

def checkOutSuccessPage(request):
    categories = Categories.objects.filter(is_active=True)

    context = {
        'page_title': f'{APP_NAME} | Гарного дня',
        'page_categories': categories,
    }
    return render(request, 'shop/checkout_success.html', context=context)