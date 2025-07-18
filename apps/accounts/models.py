from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        extra_fields.setdefault('is_active', True)
        return self.model(username=username, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)



class ProductCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name



class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, unique=True)
    category = models.ForeignKey('ProductCategory', on_delete=models.SET_NULL, null=True, blank=True)
    address_name = models.CharField(max_length=255)
    address_lat = models.FloatField(null=True, blank=True)
    address_long = models.FloatField(null=True, blank=True)

    is_approved = models.BooleanField(default=False)  # admin tasdiqlashi kerak
    is_active = models.BooleanField(default=False)    # tasdiqlanmasa, login qilolmaydi
    is_seller = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email', 'phone_number']

    def __str__(self):
        return self.username


