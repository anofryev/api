import requests

from celery import shared_task
from decimal import Decimal

from django.utils import timezone

from apps.accounts.models import Doctor
from .models import MoleImage, Study
from .models.study import ParticipantNotificationDocConsentUpdate, \
    DoctorNotificationDocConsentUpdate


class GetPredictionError(Exception):
    pass


@shared_task
def get_mole_image_prediction(pk):
    mole_image = MoleImage.objects.get(pk=pk)

    payload = {
        'image_url': mole_image.photo.url,
    }
    url = 'http://52.36.205.204/mole_classifier_url'
    r = requests.post(url, json=payload)

    if r.json()['status'] == 'success':
        mole_image.prediction = r.json()['prediction']
        mole_image.prediction_accuracy = Decimal(r.json()['probability'])
        mole_image.save()
    else:
        raise GetPredictionError(r)


def get_study_context(study):
    return {
        'study_title': study.title,
        'study_date_of_change': timezone.now().strftime('%m/%d/%Y %H:%M'),
        'study_coordinator': study.author.doctor_ptr.get_full_name(),
        'study_coordinator_email': study.author.doctor_ptr.email
    }


@shared_task
def send_participant_consent_changed(study_pk, participant_pk):
    # TODO: Add attachment to email
    study = Study.objects.get(pk=study_pk)
    participant = Doctor.objects.get(pk=participant_pk)

    ParticipantNotificationDocConsentUpdate(
        context=get_study_context(study)).send([participant.email])


@shared_task
def send_doctor_consent_changed(study_pk, doctor_pk):
    study = Study.objects.get(pk=study_pk)
    doctor = Doctor.objects.get(pk=doctor_pk)

    context = get_study_context(study)
    context.update({'username': doctor.username})
    DoctorNotificationDocConsentUpdate(context=context).send([doctor.email])
