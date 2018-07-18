from django.db import models
from ckeditor.fields import RichTextField


class FlatBlock(models.Model):
    slug = models.CharField(
        max_length=80,
        unique=True)
    content = RichTextField()

    def __str__(self):
        return self.slug
