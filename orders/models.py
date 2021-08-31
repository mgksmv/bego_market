from django.db import models

from accounts.models import Account
from store.models import Product


class Order(models.Model):
    STATUS = (
        ('Новый заказ', 'Новый заказ'),
        ('Принят', 'Принят'),
        ('Вручён', 'Вручён'),
        ('Отменён', 'Отменён'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь')
    order_number = models.CharField(max_length=20, verbose_name='Номер заказа')
    first_name = models.CharField(max_length=75, verbose_name='Имя')
    last_name = models.CharField(max_length=75, verbose_name='Фамилия')
    email = models.CharField(max_length=100, verbose_name='E-mail')
    phone = models.CharField(max_length=15, verbose_name='Номер телефона')
    city = models.CharField(max_length=100, verbose_name='Город/Населённый пункт')
    street = models.CharField(max_length=200, verbose_name='Улица')
    order_note = models.TextField(max_length=200, blank=True, verbose_name='Примечание к заказу')
    order_total = models.FloatField(verbose_name='Итого к оплате')
    status = models.CharField(max_length=15, choices=STATUS, default='Новый заказ', verbose_name='Статус')
    ip = models.CharField(max_length=20, blank=True, verbose_name='IP')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.first_name


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.IntegerField(verbose_name='Количество')
    product_price = models.FloatField(verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.product.product_name
