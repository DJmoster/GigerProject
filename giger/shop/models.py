from django.db import models
from django.urls import reverse


class Products(models.Model):
    '''Таблиця наявних товарів'''
    category_id = models.ForeignKey('Categories', on_delete=models.PROTECT)
    vendor_id   = models.ForeignKey('Vendors', on_delete=models.PROTECT)

    name = models.CharField(max_length=255)
    sku  = models.CharField(max_length=255)

    description_short = models.TextField()
    description       = models.TextField()

    # Під замовлення: -1; Немає в наявності: 0;
    availability = models.IntegerField(default=-1)

    is_active    = models.BooleanField(default=True)
    price        = models.FloatField()

    url_slug      = models.SlugField(max_length=255, db_index=True, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.url_slug})
    
    @property
    def get_price(self):
        return f'{round(self.price, 10)}'.replace('.', ',') + ' грн.'
    
    @property
    def get_product_image(self):
        return ProductImages.objects.filter(product_id=self.pk).first()
    
    @property
    def get_reviews_avg(self):
        reviews       = ProductReviews.objects.filter(product_id=self.pk)
        reviews_sum   = len(reviews)
        reviews_count = []
        reviews_avg   = 0

        if reviews_sum != 0:
            for i in range(1,6):
                reviews_count.append(len(reviews.filter(rate=i)))

            reviews_count.reverse()

            reviews_avg = round((reviews_count[0] * 5 + 
                        reviews_count[1] * 4 + 
                        reviews_count[2] * 3 + 
                        reviews_count[3] * 2 + 
                        reviews_count[4] * 1) / reviews_sum, 1)
            
            return reviews_avg
        return None
    
    @property
    def get_reviews_count(self):
        reviews = ProductReviews.objects.filter(product_id=self.pk)

        return len(reviews)
    
    @property
    def get_reviews_division(self):
        reviews       = ProductReviews.objects.filter(product_id=self.pk)
        reviews_sum   = len(reviews)
        reviews_count = []

        if reviews_sum != 0:
            for i in range(1,6):
                reviews_count.append(len(reviews.filter(rate=i)))

            reviews_count.reverse()
            return reviews_count
        return None

    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'

class Categories(models.Model):
    '''Таблиця категорій та підкатегорій'''
    parent_id  = models.ForeignKey('Categories', null=True, blank=True, on_delete=models.PROTECT)
    hotline_id = models.IntegerField(null=True, blank=True)

    name      = models.CharField(max_length=255)

    url_slug  = models.SlugField(max_length=255, db_index=True, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.url_slug})
    
    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

class Vendors(models.Model):
    '''Таблиця наявних вендорів'''
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Вендор'
        verbose_name_plural = 'Вендори'

class ProductImages(models.Model):
    '''Таблиця зображень товару'''
    product_id = models.ForeignKey('Products', on_delete=models.CASCADE)
    image      = models.ImageField(upload_to='product_photos/%Y/%m/')

class ProductSales(models.Model):
    '''Таблиця для знижок на товар'''
    product_id = models.ForeignKey('Products', on_delete=models.CASCADE)
    end_date   = models.DateTimeField()
    price      = models.FloatField()

class ProductReviews(models.Model):
    '''Таблиця відгуків на товар'''
    product_id = models.ForeignKey('Products', on_delete=models.CASCADE)
    
    name        = models.CharField(max_length=255)
    email       = models.EmailField(max_length=255)
    description = models.TextField()
    rate        = models.IntegerField()
    creation_date = models.DateField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'

class Customers(models.Model):
    '''Таблиця клієнтів що робили замовлення'''
    name    = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone   = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.name} {self.surname} {self.phone}'
    
    class Meta:
        verbose_name = 'Клієнт'
        verbose_name_plural = 'Клієнти'


class Orders(models.Model):
    '''Таблиця замовлень'''
    STATUSES = [
        ('Н', 'НОВЕ'),
        ('П', 'ПРИЙНЯТЕ'),
        ('З', 'ЗАМОВЛЕНЕ'),
        ('ВПД', 'В ПРОЦЕСІ ДОСТАВКИ'),
        ('В', 'ВІДПРАВЛЕНЕ'),
        ('ЗАВ', 'ЗАВЕРШЕНЕ'),
    ]

    customer_id = models.ForeignKey('Customers', on_delete=models.PROTECT)

    status = models.CharField(max_length=255, choices=STATUSES, default='Н')
    notes  = models.TextField()
    shipping_method = models.CharField(max_length=255)

    date_created = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.customer_id.name + ' ' + self.customer_id.surname
    
    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'

class OrderItems(models.Model):
    '''Таблиця товарів які людина замовила'''
    product_id = models.ForeignKey('Products', blank=True, null=True, on_delete=models.SET_NULL)
    order_id   = models.ForeignKey('Orders', on_delete=models.CASCADE)

    name         = models.CharField(max_length=255)
    buying_price = models.FloatField()
    count        = models.IntegerField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'

class ItemWarranty(models.Model):
    '''Таблиця наявних гарантій на товари'''
    order_item_id = models.ForeignKey('OrderItems', on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=255)

    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()

    def __str__(self):
        return self.serial_number
