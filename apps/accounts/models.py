from common.validators import icon_extensions
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from store.models import Category

from .managers import CustomUserManager


class Address(models.Model):
    name = models.CharField(max_length=255)
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        SUPER_ADMIN = "super_admin", "Super admin"
        ADMIN = "admin", "Admin"
        SELLER = "seller", "Sotuvchi"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    full_name = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, unique=True)
    profile_photo = models.ImageField(
        upload_to="profiles/", null=True, blank=True, validators=[icon_extensions]
    )
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.SELLER)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "phone_number"

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.full_name} ({self.phone_number})"

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
