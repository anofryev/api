from django.db import models

from .doctor import Doctor


class Site(models.Model):
    title = models.CharField(
        max_length=120)


class Coordinator(models.Model):
    doctor_ptr = models.OneToOneField(
        Doctor,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='coordinator_role'
    )
    site = models.OneToOneField(
        Site,
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='site_coordinator'
    )

    class Meta:
        verbose_name = 'Coordinator'
        verbose_name_plural = 'Coordinators'
