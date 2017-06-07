import requests

from celery import shared_task
from decimal import Decimal

from .models import MoleImage


@shared_task
def get_mole_image_prediction(pk):
    try:
        mole_image = MoleImage.objects.get(pk=pk)
    except MoleImage.DoesNotExist:
        return

    payload = {
        'image_url': mole_image.photo.url,
    }
    url = 'http://52.36.205.204/mole_classifier_url'
    r = requests.post(url, json=payload)

    if r.json()['status'] == 'success':
        mole_image.prediction = r.json()['prediction']
        mole_image.prediction_accuracy = Decimal(r.json()['probability'])
        mole_image.save()
