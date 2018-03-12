from django.db import models
from django.db.models import Count, Max, Case, When, Q, F
from versatileimagefield.fields import VersatileImageField

from apps.main.storages import private_storage
from apps.main.models.mixins import DelayedSaveFilesMixin
from .doctor import Doctor
from .upload_paths import patient_photo_path
from .enums import SexEnum, RaceEnum


class PatientQuerySet(DelayedSaveFilesMixin, models.QuerySet):
    def annotate_moles_images_count(self):
        return self.annotate(
            moles_images_count=Count('moles__images'))

    def annotate_last_upload(self):
        return self.annotate(
            last_upload=Max('moles__images__date_created'))

    def annotate_clinical_diagnosis_required(self):
        return self.annotate(
            moles_images_with_clinical_diagnosis_required=Count(
                Case(
                    When(
                        Q(moles__images__clinical_diagnosis__exact=''),
                        then=F('moles__images__pk')
                    ),
                    default=None
                ),
                distinct=True
            )
        )

    def annotate_pathological_diagnosis_required(self):
        return self.annotate(
            moles_images_with_pathological_diagnosis_required=Count(
                Case(
                    When(
                        moles__images__biopsy=True,
                        moles__images__path_diagnosis__exact='',
                        then=F('moles__images__pk')
                    ),
                    default=None
                ),
                distinct=True
            )
        )

    def annotate_biopsy_count(self):
        return self.annotate(
            moles_images_biopsy_count=Count(
                Case(
                    When(
                        moles__images__biopsy=True,
                        then=F('moles__images__pk')
                    ),
                    default=None
                ),
                distinct=True
            )
        )

    def annotate_approve_required(self):
        return self.annotate(
            moles_images_approve_required=Count(
                Case(
                    When(moles__images__approved__exact=False,
                         then=F('moles__images__pk')),
                    default=None
                ),
                distinct=True
            )
        )


class Patient(models.Model):
    first_name = models.TextField(
        verbose_name='Encrypted first name'
    )
    last_name = models.TextField(
        verbose_name='Encrypted last name'
    )
    date_of_birth = models.TextField(
        verbose_name='Encrypted date of birth',
        blank=True, null=True
    )
    mrn = models.TextField(
        null=True,
        blank=True,
        verbose_name='Encrypted Medical Record Number'
    )
    mrn_hash = models.CharField(
        max_length=32,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Medical Record Number'
    )
    photo = VersatileImageField(
        verbose_name='Profile Picture',
        upload_to=patient_photo_path,
        storage=private_storage,
        max_length=300,
        null=True,
        blank=True
    )
    sex = models.CharField(
        max_length=1,
        choices=SexEnum.CHOICES,
        verbose_name='Sex',
        blank=True, null=True
    )
    race = models.SmallIntegerField(
        choices=RaceEnum.CHOICES,
        verbose_name='Race',
        blank=True, null=True
    )
    doctors = models.ManyToManyField(
        Doctor,
        related_name="patients",
        through='DoctorToPatient'
    )
    objects = PatientQuerySet.as_manager()

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'

    @property
    def valid_consent(self):
        return self.consents.valid().first()

    def __str__(self):
        return "Patient: {0} ({1},{2})".format(
            self.pk,
            self.get_race_display(),
            self.get_sex_display())


class DoctorToPatient(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        verbose_name='Patient'
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        verbose_name='Doctor'
    )

    encrypted_key = models.TextField(
        verbose_name='Encrypted key for patient data',
    )
