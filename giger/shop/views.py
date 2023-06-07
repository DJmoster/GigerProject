from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator

from shop.models import Products, ProductImages, ProductReviews, Categories

def error404Page(request, exception):
    context = {
        'page_title': 'Giger | 404',
    }
    return render(request, 'shop/error.html', context=context)

def homePage(request):
    context = {
        'page_title': 'Giger | Home',
    }
    return render(request, 'shop/home.html', context=context)

def productPage(request, product_slug):
    product = get_object_or_404(
        Products, 
        url_slug=product_slug, 
        is_active=True, 
        category_id__is_active=True
    )

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

    context = {
        'page_title': 'Giger | ' + product.name,
        'product_object': product,
        'product_images': images,
        'product_reviews': reviews,
    }

    return render(request, 'shop/product.html', context=context)

def categoryPage(request, category_slug):
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
        'page_title': f'Giger | {category.name}',
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
        'page_title': f'Giger | Пошук',
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
            'price': product.get_price,
            'image': product.get_product_image.image.url,
            'availability': product.availability,
        }
    }

    return JsonResponse(response)

def wishlistPage(request):

    context = {
        'page_title': f'Giger | Список бажаного',
    }
    return render(request, 'shop/wishlist.html', context=context)