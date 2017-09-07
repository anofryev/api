from django.db import models
from django.db.models import Max
from django.contrib.postgres.fields import JSONField

from apps.accounts.models import Patient
from .anatomical_site import AnatomicalSite
from .patient_anatomical_site import PatientAnatomicalSite


class MoleQuerySet(models.QuerySet):
    def annotate_last_upload(self):
        return self.annotate(last_upload=Max('images__date_created'))


class Mole(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='moles',
        verbose_name='Patient'
    )
    anatomical_site = models.ForeignKey(
        AnatomicalSite,
        verbose_name='Anatomical site'
    )
    patient_anatomical_site = models.ForeignKey(
        PatientAnatomicalSite,
        verbose_name='Patient anatomical site',
        blank=True,
        null=True
    )
    position_info = JSONField(
        verbose_name='Mole position information'
    )
    objects = MoleQuerySet.as_manager()

    class Meta:
        verbose_name = 'Mole'
        verbose_name_plural = 'Moles'

    def __str__(self):
        return '{0}: {1}'.format(self.patient, self.anatomical_site)

    @property
    def anatomical_sites(self):
        return list(
            self.anatomical_site.get_ancestors()) + [self.anatomical_site]

    @property
    def last_image(self):
        try:
            return self.images.latest('date_created')
        except models.ObjectDoesNotExist:
            return None
