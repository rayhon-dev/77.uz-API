from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from .manager import CustomUserManager
from store.models import Category


class Address(models.Model):
    name = models.CharField(max_length=255)
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name



class CustomUser(AbstractBaseUser):
    full_name = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profiles/', null=True, blank=True)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    manual_password = models.CharField(max_length=128, blank=True, null=True)


    is_active = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser