from django.db import models
from django.urls import reverse
from django.conf import settings
from ckeditor.fields import RichTextField

from category.models import Category


class Brand(models.Model):
    brand_name = models.CharField(max_length=255, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL')
    logo = models.ImageField(upload_to='images/brands', verbose_name='Логотип')
    country = models.CharField(max_length=255, verbose_name='Страна')
    description = RichTextField(verbose_name='Описание')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    class Meta:
        verbose_name = 'бренд'
        verbose_name_plural = 'Бренды'

    def get_url(self):
        return reverse('brand_detail', args=[self.slug])

    def __str__(self):
        return self.brand_name


class Product(models.Model):
    product_name = models.CharField(max_length=255, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='URL')
    description = RichTextField(verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')
    images = models.ImageField(upload_to='images/products', verbose_name='Изображение')
    stock = models.IntegerField(verbose_name='Запас на складе')
    is_available = models.BooleanField(default=True, verbose_name='В наличии')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Бренд')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'Товары'

    def get_url(self):
        return reverse('product_detail', args=[self.slug])

    def __str__(self):
        return self.product_name
