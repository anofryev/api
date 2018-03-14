from django.db import models

from .doctor import Doctor
from .patient import Patient


# Physician is a patient, who can log in into system (so, can be a doctor)
class Physician(models.Model):
    doctor_ptr = models.OneToOneField(
        Doctor,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='physician_role'
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.doctor_ptr.__str__()

    class Meta:
        verbose_name = 'Physician'
        verbose_name_plural = 'Physician'
