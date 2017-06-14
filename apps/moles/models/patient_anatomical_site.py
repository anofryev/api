from django.db import models
from versatileimagefield.fields import VersatileImageField

from apps.main.storages import private_storage
from apps.main.models.mixins import DelayedSaveFilesMixin
from apps.accounts.models import Patient
from .anatomical_site import AnatomicalSite
from .upload_paths import distant_photo_path


class PatientAnatomicalSite(DelayedSaveFilesMixin, models.Model):
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
        storage=private_storage,
        max_length=300,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Patient anatomical site'
        verbose_name_plural = 'Patient anatomical sites'

    def __str__(self):
        return '{0}: {1}'.format(self.patient, self.anatomical_site)
