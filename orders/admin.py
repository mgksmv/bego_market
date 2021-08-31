from django.contrib import admin
from django.utils.html import format_html

from .models import Order, OrderProduct


class OrderProductInline(admin.TabularInline):
    def thumbnail(self, object):
        return format_html(f'<img src="{object.product.images.url}" width="100" />')

    thumbnail.short_description = 'Фото'

    model = OrderProduct
    readonly_fields = ('user', 'thumbnail', 'product', 'quantity', 'product_price')
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'first_name', 'last_name', 'email', 'phone', 'city', 'street', 'order_total', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['order_number', 'first_name', 'last_name', 'email', 'phone']
    list_per_page = 20
    inlines = [OrderProductInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
