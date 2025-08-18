from common.models import BaseModel, Region
from common.validators import icon_extensions
from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Category(BaseModel):
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="child",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=255)
    icon = models.FileField(
        upload_to="categories/", validators=[icon_extensions], null=True, blank=True
    )

    def __str__(self):
        return getattr(self, "name", "Category")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Ad(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("pending", "Pending"),
        ("rejected", "Rejected"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    price = models.PositiveIntegerField()
    category = models.ForeignKey("store.Category", on_delete=models.CASCADE)
    seller = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    address = models.ForeignKey("accounts.Address", on_delete=models.CASCADE)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField("accounts.CustomUser", related_name="liked_ads", blank=True)
    is_top = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_uz)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class AdPhoto(models.Model):
    ad = models.ForeignKey(Ad, related_name="photos", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/")
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class FavouriteProduct(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favourites",
        null=True,
        blank=True,
    )
    device_id = models.CharField(max_length=255, null=True, blank=True)
    product = models.ForeignKey("store.Ad", on_delete=models.CASCADE, related_name="favourites")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"],
                name="unique_user_product",
                condition=models.Q(user__isnull=False),
            ),
            models.UniqueConstraint(
                fields=["device_id", "product"],
                name="unique_device_product",
                condition=models.Q(device_id__isnull=False),
            ),
        ]

    def __str__(self):
        return f"{self.user or self.device_id} - {self.product}"


class MySearch(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="my_searches"
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    search_query = models.CharField(max_length=255, blank=True, null=True)
    price_min = models.PositiveIntegerField(null=True, blank=True)
    price_max = models.PositiveIntegerField(null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.search_query or ''}"


class SearchQuery(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class SearchCount(models.Model):
    product = models.OneToOneField(
        "store.Ad", on_delete=models.CASCADE, related_name="search_count_obj"
    )
    search_count = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} ({self.search_count})"
