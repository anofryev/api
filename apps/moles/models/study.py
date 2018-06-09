from django.db import models
from django.db.models.signals import m2m_changed
from django.utils import timezone
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
        # TODO: 1. Add send email as celery task
        # TODO: 2. Add attachment to email
        context_var = {
            'study_title': self.title,
            'study_date_of_change': timezone.now().strftime('%m/%d/%Y %H:%M'),
            'study_coordinator': self.author.doctor_ptr.get_full_name(),
            'study_coordinator_email': self.author.doctor_ptr.email
        }

        for study_to_patient in StudyToPatient.objects.filter(study=self):
            if study_to_patient.patient_consent:
                study_to_patient.patient_consent.date_expired = timezone.now()
                study_to_patient.patient_consent.save()
                participant = get_participant_doctor(study_to_patient.patient)
                if participant:
                    ParticipantNotificationDocConsentUpdate(
                        context=context_var).send([participant.email])

        for doctor in self.doctors.all():
            doctor_context = context_var
            doctor_context.update({'username': doctor.username})
            DoctorNotificationDocConsentUdate(context=doctor_context)\
                .send([doctor.email])


    class Meta:
        verbose_name = 'Study'
        verbose_name_plural = 'Studies'


class ConsentDoc(models.Model, ThumbnailMixin):
    ATTACHMENT_FIELD_NAME = 'file'

    file = models.FileField(
        verbose_name='Document file',
        upload_to=study_consent_docs_path,
        storage=private_storage,
    )
    original_filename = models.CharField(
        max_length=250,
        blank=True, null=True)

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


class DoctorNotificationDocConsentUdate(BaseEmailMessage):
    template_name = 'email/doctor_notification_doc_consent_update.html'


class ParticipantNotificationDocConsentUpdate(BaseEmailMessage):
    template_name = 'email/participant_notification_doc_consent_update.html'
