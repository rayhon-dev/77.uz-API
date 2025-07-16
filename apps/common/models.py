import uuid
from django.utils.text import slugify
from django.db import models


class BaseModel(models.Model):
    guid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, db_index=True
    )
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Page(BaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.SlugField(unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title_uz or self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title