from decimal import Decimal

from django.contrib.postgres.fields import JSONField
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from versatileimagefield.fields import VersatileImageField

from apps.main.storages import private_storage
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
        storage=private_storage,
        max_length=300,
        blank=True,
        null=True
    )
    biopsy = models.BooleanField(
        default=False,
        verbose_name='Biopsy'
    )
    biopsy_data = JSONField(
        blank=True,
        null=True,
        verbose_name='Biopsy data'
    )
    approved = models.BooleanField(
        verbose_name='Photo is approved by coordinator',
        default=False)

    class Meta:
        verbose_name = 'Mole image'
        verbose_name_plural = 'Mole images'
        ordering = ('-date_created',)

    def __str__(self):
        return str(self.mole)


@receiver(post_save, sender=MoleImage)
def set_up(sender, instance, created, **kwargs):
    """
    Completes MoleImage instance after creation by calling delayed task
    """
    from ..tasks import get_mole_image_prediction

    if created:
        transaction.on_commit(
            lambda: get_mole_image_prediction.delay(pk=instance.pk))
