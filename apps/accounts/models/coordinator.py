from django.db import models

from .doctor import Doctor


class Coordinator(models.Model):
    doctor_ptr = models.OneToOneField(
        Doctor,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='coordinator_role'
    )

    class Meta:
        verbose_name = 'Coordinator'
        verbose_name_plural = 'Coordinators'
