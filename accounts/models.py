from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class AccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('Пользователь должен иметь E-mail адрес!')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True, verbose_name='Логин')
    first_name = models.CharField(max_length=75, verbose_name='Имя')
    last_name = models.CharField(max_length=75, verbose_name='Фамилия')
    email = models.EmailField(max_length=100, unique=True, verbose_name='E-mail')
    phone_number = models.CharField(max_length=15, verbose_name='Номер телефона', blank=True)
    city = models.CharField(max_length=255, verbose_name='Город')
    street = models.CharField(max_length=255, blank=True, verbose_name='Улица')

    # required
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    last_login = models.DateTimeField(auto_now=True, verbose_name='Последний вход')
    is_active = models.BooleanField(default=False, verbose_name='Активный')
    is_staff = models.BooleanField(default=False, verbose_name='Статус персонала')
    is_admin = models.BooleanField(default=False, verbose_name='Статус админа')
    is_superadmin = models.BooleanField(default=False, verbose_name='Статус суперпользователя')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = AccountManager()

    class Meta:
        verbose_name = 'аккаунт'
        verbose_name_plural = 'Аккаунты'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
