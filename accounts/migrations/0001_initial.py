# Generated by Django 3.2.4 on 2021-07-27 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('username', models.CharField(max_length=100, unique=True, verbose_name='Логин')),
                ('first_name', models.CharField(max_length=75, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=75, verbose_name='Фамилия')),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='E-mail')),
                ('phone_number', models.CharField(blank=True, max_length=15, verbose_name='Номер телефона')),
                ('city', models.CharField(max_length=255, verbose_name='Город')),
                ('street', models.CharField(blank=True, max_length=255, verbose_name='Улица')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='Последний вход')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активный')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Статус персонала')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Статус админа')),
                ('is_superadmin', models.BooleanField(default=False, verbose_name='Статус суперпользователя')),
            ],
            options={
                'verbose_name': 'аккаунт',
                'verbose_name_plural': 'Аккаунты',
            },
        ),
    ]