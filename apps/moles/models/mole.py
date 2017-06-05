from django.db import models

from apps.accounts.models import Patient
from .anatomical_site import AnatomicalSite


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
