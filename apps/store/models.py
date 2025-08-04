from django.db import models
from common.models import BaseModel
from common.validators import icon_extensions
from django.utils.text import slugify
from accounts.models import CustomUser, Address


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
        upload_to='categories/', validators=[icon_extensions], null=True, blank=True
    )

    def __str__(self):
        return getattr(self, 'name', 'Category')

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Ad(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    price = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_uz)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class AdPhoto(models.Model):
    ad = models.ForeignKey(Ads, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
