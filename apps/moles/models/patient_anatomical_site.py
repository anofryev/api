from django.db import models
from versatileimagefield.fields import VersatileImageField

from apps.accounts.models import Patient
from .anatomical_site import AnatomicalSite
from .upload_paths import distant_photo_path


class PatientAnatomicalSite(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='anatomical_sites',
        verbose_name='Patient'
    )
    anatomical_site = models.ForeignKey(
        AnatomicalSite,
        on_delete=models.CASCADE,
        verbose_name='Anatomical site'
    )
    distant_photo = VersatileImageField(
        verbose_name='Distant photo',
        upload_to=distant_photo_path,
        max_length=300,
        blank=True,
        null=True
    )
