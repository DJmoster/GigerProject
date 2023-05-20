# Generated by Django 4.2.1 on 2023-05-20 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotline_id', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('url_slug', models.SlugField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('parent_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='shop.categories')),
            ],
        ),
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('sku', models.CharField(max_length=255)),
                ('description_short', models.TextField()),
                ('description', models.TextField()),
                ('availability', models.IntegerField(default=-1)),
                ('is_active', models.BooleanField(default=True)),
                ('price', models.FloatField()),
                ('url_slug', models.SlugField(max_length=255, unique=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.categories')),
            ],
        ),
        migrations.CreateModel(
            name='Vendors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ProductSales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('end_date', models.DateTimeField()),
                ('price', models.FloatField()),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.products')),
            ],
        ),
        migrations.AddField(
            model_name='products',
            name='vendor_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.vendors'),
        ),
        migrations.CreateModel(
            name='ProductReviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('description', models.TextField()),
                ('rate', models.IntegerField()),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.products')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_photos/%Y/%m/')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.products')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Н', 'НОВЕ'), ('П', 'ПРИЙНЯТЕ'), ('З', 'ЗАМОВЛЕНЕ'), ('ВПД', 'В ПРОЦЕСІ ДОСТАВКИ'), ('В', 'ВІДПРАВЛЕНЕ'), ('ЗАВ', 'ЗАВЕРШЕНЕ')], default='Н', max_length=255)),
                ('notes', models.TextField()),
                ('shipping_method', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.customers')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('buying_price', models.FloatField()),
                ('count', models.IntegerField()),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.orders')),
                ('product_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.products')),
            ],
        ),
        migrations.CreateModel(
            name='ItemWarranty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(max_length=255)),
                ('start_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField()),
                ('order_item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.orderitems')),
            ],
        ),
    ]