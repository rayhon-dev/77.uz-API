import uuid

from django.db import models
from django.utils.text import slugify


class BaseModel(models.Model):
    guid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Page(BaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Region(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class District(BaseModel):
    region = models.ForeignKey(Region, related_name="districts", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Setting(models.Model):
    phone = models.CharField(max_length=100)
    support_email = models.EmailField()
    working_hours = models.CharField(max_length=100)
    app_version = models.CharField(max_length=100)
    maintenance_mode = models.BooleanField(default=False)

    def __str__(self):
        return "Site Settings"
