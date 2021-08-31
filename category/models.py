from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                            verbose_name='Родительская категория')
    category_name = models.CharField(max_length=255, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL')
    image = models.ImageField(upload_to='images/categories', default='images/categories/default.png', blank=True,
                              verbose_name='Картинка')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    class MPTTMeta:
        order_insertion_by = ['category_name']

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name
