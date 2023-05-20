from django.contrib import admin
from shop.models import *

class ProductImagesInline(admin.TabularInline):
    model = ProductImages

class ProductSalesInline(admin.TabularInline):
    model = ProductSales
    extra = 1

class ProductsAdmin(admin.ModelAdmin):
    search_fields = ('name', 'sku', 'price')

    list_display = ('name', 'sku', 'availability', 'price', 'is_active')
    list_display_links = ('name',)
    list_editable = ('sku', 'availability', 'price', 'is_active')
    list_filter = ('availability', 'price', 'is_active')

    inlines = [ProductImagesInline, ProductSalesInline]
    prepopulated_fields = {'url_slug': ('name',)}

class CategoriesAdmin(admin.ModelAdmin):
    search_fields = ('name', 'url_slug', 'hotline_id')

    list_display = ('name', 'hotline_id', 'is_active')
    list_display_links = ('name',)
    list_editable = ('hotline_id', 'is_active')
    list_filter = ('is_active',)

    prepopulated_fields = {'url_slug': ('name',)}


admin.site.register(Products, ProductsAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Vendors)

# class ItemWarrantyInline(admin.TabularInline):
#     model = ItemWarranty
#     extra = 1

# class OrderItemsAdmin(admin.ModelAdmin):
#     inlines = [ItemWarrantyInline]

class OrderItemsInline(admin.TabularInline):
    model = OrderItems

class OrdersAdmin(admin.ModelAdmin):
    search_fields = ('customer_id__name', 'customer_id__surname', 'customer_id__phone')

    inlines = [OrderItemsInline]

admin.site.register(Orders, OrdersAdmin)
admin.site.register(Customers)
# admin.site.register(OrderItems, OrderItemsAdmin) TODO

