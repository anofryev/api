from django.conf.urls import url, include
from rest_framework import routers

from .viewsets import *


patient_router = routers.SimpleRouter()
patient_router.register('anatomical_site', PatientAnatomicalSiteViewSet)
patient_router.register('mole', MoleViewSet)

urlpatterns = [
    url(r'^patient/(?P<patient_pk>\d+)/',
        include(patient_router.urls)),
]
