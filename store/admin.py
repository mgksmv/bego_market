from django.contrib import admin
from django.utils.html import format_html

from .models import Product, Brand


class ProductAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html(f'<img src="{object.images.url}" width="100" />')

    list_display = ('thumbnail', 'product_name', 'price', 'stock', 'category', 'brand', 'created_date', 'modified_date')
    list_display_links = ('thumbnail', 'product_name')
    readonly_fields = ('created_date', 'modified_date')
    prepopulated_fields = {'slug': ('product_name',)}


class BrandAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html(f'<img src="{object.logo.url}" width="100" />')

    thumbnail.short_description = 'Фото'

    list_display = ('thumbnail', 'brand_name', 'country')
    list_display_links = ('thumbnail', 'brand_name')
    readonly_fields = ('created_date', 'modified_date')
    prepopulated_fields = {'slug': ('brand_name',)}


admin.site.register(Product, ProductAdmin)
admin.site.register(Brand, BrandAdmin)
