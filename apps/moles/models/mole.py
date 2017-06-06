from django.db import models

from apps.accounts.models import Patient
from .anatomical_site import AnatomicalSite
from .patient_anatomical_site import PatientAnatomicalSite


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
    position_x = models.IntegerField(
        verbose_name='Position x'
    )
    position_y = models.IntegerField(
        verbose_name='Position y'
    )

    class Meta:
        verbose_name = 'Mole'
        verbose_name_plural = 'Moles'

    def __str__(self):
        return '{0}: {1}'.format(self.patient, self.anatomical_site)

    @property
    def patient_anatomical_site(self):
        return PatientAnatomicalSite.objects.filter(
            patient=self.patient, anatomical_site=self.anatomical_site).first()
