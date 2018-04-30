from django.db import models
from django.db.models import Max, Count, Case, When, Q, F
from django.contrib.postgres.fields import JSONField

from apps.accounts.models import Patient
from apps.main.models.aggregates import ArrayAgg, ArrayRemove
from .anatomical_site import AnatomicalSite
from .patient_anatomical_site import PatientAnatomicalSite


class MoleQuerySet(models.QuerySet):
    def annotate_last_upload(self):
        return self.annotate(last_upload=Max('images__date_created'))

    def annotate_clinical_diagnosis_required(self, study_pk):
        when = {
            'images__clinical_diagnosis__exact': '',
            'images__study_id': study_pk,
            'then': F('images__pk')
        }

        return self.annotate(
            images_with_clinical_diagnosis_required=Count(
                Case(
                    When(**when),
                    default=None
                ),
                distinct=True
            )
        )

    def annotate_pathological_diagnosis_required(self, study_pk):
        when = {
            'images__biopsy': True,
            'images__path_diagnosis__exact': '',
            'images__study_id': study_pk,
            'then': F('images__pk')
        }

        return self.annotate(
            images_with_pathological_diagnosis_required=Count(
                Case(
                    When(**when),
                    default=None
                ),
                distinct=True
            )
        )

    def annotate_biopsy_count(self, study_pk):
        when = {
            'images__biopsy': True,
            'images__study_id': study_pk,
            'then': F('images__pk')
        }

        return self.annotate(
            images_biopsy_count=Count(
                Case(
                    When(**when),
                    default=None
                ),
                distinct=True
            )
        )

    def annotate_approve_required(self, study_pk):
        when = {
            'images__approved__exact': False,
            'images__study_id': study_pk,
            'then': F('images__pk')
        }

        return self.annotate(
            images_approve_required=Count(
                Case(
                    When(**when),
                    default=None
                ),
                distinct=True
            )
        )

    def annotate_studies(self):
        return self.annotate(
            studies=ArrayRemove(
                ArrayAgg(
                    'images__study_id',
                    distinct=True
                ),
                None
            )
        )

    def annotate_images_count(self, study_pk):
        return self.annotate(
            images_count=Count(
                Case(
                    When(images__study_id=study_pk,
                         then=F('images__pk')),
                    default=None
                ),
                distinct=True
            )
        )


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
