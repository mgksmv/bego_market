# Generated by Django 3.2.4 on 2021-07-27 07:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=20, verbose_name='Номер заказа')),
                ('first_name', models.CharField(max_length=75, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=75, verbose_name='Фамилия')),
                ('email', models.CharField(max_length=100, verbose_name='E-mail')),
                ('phone', models.CharField(max_length=15, verbose_name='Номер телефона')),
                ('city', models.CharField(max_length=100, verbose_name='Город/Населённый пункт')),
                ('street', models.CharField(max_length=200, verbose_name='Улица')),
                ('order_note', models.TextField(blank=True, max_length=200, verbose_name='Примечание к заказу')),
                ('order_total', models.FloatField(verbose_name='Итого к оплате')),
                ('status', models.CharField(choices=[('Новый заказ', 'Новый заказ'), ('Принят', 'Принят'), ('Вручён', 'Вручён'), ('Отменён', 'Отменён')], default='Новый заказ', max_length=15, verbose_name='Статус')),
                ('ip', models.CharField(blank=True, max_length=20, verbose_name='IP')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='Количество')),
                ('product_price', models.FloatField(verbose_name='Цена')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='Товар')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'Товары',
            },
        ),
    ]