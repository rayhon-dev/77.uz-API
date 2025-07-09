import uuid

from django.db import models


class BaseModel(models.Model):
    guid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, db_index=True
    )
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Page(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
