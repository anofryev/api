from django.db import models
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey


class AnatomicalSite(MPTTModel):
    slug = models.SlugField(
        verbose_name='Slug',
        primary_key=True,
        editable=False
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Name'
    )
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        verbose_name='Parent anatomical site',
        related_name='children',
        db_index=True
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        return super(AnatomicalSite, self).save(*args, **kwargs)
