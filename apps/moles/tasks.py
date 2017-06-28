import requests

from celery import shared_task
from decimal import Decimal

from .models import MoleImage


class GetPrerdictionError(Exception):
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
        raise GetPrerdictionError(r)
