from django.db import models

from store.models import Product, Brand
from accounts.models import Account


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True, verbose_name='ID корзины')
    date_added = models.DateField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, verbose_name='Корзина')
    quantity = models.IntegerField(verbose_name='Количество')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        verbose_name = 'экземпляр корзина'
        verbose_name_plural = 'Экземпляры корзины'

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.product}'


class Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')

    class Meta:
        verbose_name = 'список желаемого'
        verbose_name_plural = 'Список желаемого'

    def __str__(self):
        return f'{self.user} / {self.product}'
