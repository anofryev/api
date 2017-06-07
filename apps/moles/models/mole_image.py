from decimal import Decimal

from django.db import models
from versatileimagefield.fields import VersatileImageField

from .mole import Mole
from .upload_paths import mole_image_photo_path


class MoleImage(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    mole = models.ForeignKey(
        Mole,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Mole'
    )
    path_diagnosis = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Path diagnosis'
    )
    clinical_diagnosis = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Clinical diagnosis'
    )
    prediction = models.CharField(
        max_length=100,
        default='Unknown',
        blank=True,
        verbose_name='Prediction'
    )
    prediction_accuracy = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        blank=True,
        null=True,
        default=Decimal(0.000),
        verbose_name='Prediction accuracy'
    )
    photo = VersatileImageField(
        verbose_name='Photo',
        upload_to=mole_image_photo_path,
        max_length=300,
        blank=True,
        null=True
    )
    biopsy = models.BooleanField(
        default=False,
        verbose_name='Biopsy'
    )

    class Meta:
        verbose_name = 'Mole image'
        verbose_name_plural = 'Mole images'

    def __str__(self):
        return self.mole
