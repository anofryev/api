from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from templated_mail.mail import BaseEmailMessage

from apps.accounts.models import Coordinator
from apps.accounts.models.participant import get_participant_doctor
from apps.main.models.mixins.thumbnail import ThumbnailMixin
from apps.main.storages import private_storage
from apps.moles.models.upload_paths import study_consent_docs_path


class Study(models.Model):
    author = models.ForeignKey(
        Coordinator,
        related_name='studies',
        blank=True, null=True)
    title = models.CharField(
        max_length=120
    )
    doctors = models.ManyToManyField(
        'accounts.Doctor',
        blank=True,
        related_name='studies',
    )
    patients = models.ManyToManyField(
        'accounts.Patient',
        blank=True,
        related_name='studies',
        through='StudyToPatient'
    )
    consent_docs = models.ManyToManyField(
        'ConsentDoc',
        blank=True,
        related_name='studies',
    )

    def __str__(self):
        return self.title

    def invalidate_consents(self):
        from apps.moles.tasks import send_doctor_consent_changed, \
            send_participant_consent_changed

        for study_to_patient in StudyToPatient.objects.filter(study=self):
            if study_to_patient.patient_consent:
                study_to_patient.patient_consent.date_expired = timezone.now()
                study_to_patient.patient_consent.save()

                participant = get_participant_doctor(study_to_patient.patient)
                if participant:
                    send_participant_consent_changed.apply_async(
                        countdown=3,
                        args=[self.pk, participant.pk])

        for doctor_pk in self.doctors.all().values_list('pk', flat=True):
            send_doctor_consent_changed.apply_async(
                countdown=3,
                args=[self.pk, doctor_pk])

    class Meta:
        verbose_name = 'Study'
        verbose_name_plural = 'Studies'


class ConsentDoc(models.Model, ThumbnailMixin):
    ATTACHMENT_FIELD_NAME = 'file'

    file = models.FileField(
        verbose_name='Document file',
        upload_to=study_consent_docs_path,
        storage=private_storage,
        validators=[FileExtensionValidator(
            allowed_extensions=[
                'jpg', 'jpeg', 'png', 'gif', 'svg',
                'pdf', 'doc', 'docx', 'odt', 'html', 'htm', 'rtf'
            ]
        )]
    )
    original_filename = models.CharField(
        max_length=250,
        blank=True, null=True
    )
    is_default_consent = models.BooleanField(
        verbose_name='Used as part of default consent form',
        default=False
    )

    def __str__(self):
        return '{0} ({1})'.format(self.original_filename, self.pk)

    class Meta:
        verbose_name = 'Consent doc'
        verbose_name_plural = 'Consent docs'


class StudyToPatient(models.Model):
    study = models.ForeignKey(
        Study,
        on_delete=models.CASCADE,
        verbose_name='Study'
    )
    patient = models.ForeignKey(
        'accounts.Patient',
        on_delete=models.CASCADE,
        verbose_name='Patient'
    )
    patient_consent = models.ForeignKey(
        'accounts.PatientConsent',
        blank=True, null=True
    )

    def __str__(self):
        return '%s - %s' % (self.study, self.patient)


class DoctorNotificationDocConsentUpdate(BaseEmailMessage):
    template_name = 'email/doctor_notification_doc_consent_update.html'


class ParticipantNotificationDocConsentUpdate(BaseEmailMessage):
    template_name = 'email/participant_notification_doc_consent_update.html'
