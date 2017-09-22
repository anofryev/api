from django.db import models

from .doctor import Doctor


class Coordinator(models.Model):
    doctor_ptr = models.OneToOneField(
        Doctor,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='coordinator_role'
    )

    def __str__(self):
        return self.doctor_ptr.__str__()

    class Meta:
        verbose_name = 'Coordinator'
        verbose_name_plural = 'Coordinators'


class Site(models.Model):
    title = models.CharField(
        max_length=120)

    site_coordinator = models.OneToOneField(
        Coordinator,
        on_delete=models.CASCADE,
        related_name='site'
    )

    def __str__(self):
        return self.title
