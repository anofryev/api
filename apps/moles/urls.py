from django.conf.urls import url, include
from rest_framework_nested import routers

from apps.accounts.urls import router_for_patients
from .viewsets import *


patient_router = routers.NestedSimpleRouter(
    router_for_patients, r'patient', lookup='patient')
patient_router.register('anatomical_site', PatientAnatomicalSiteViewSet)
patient_router.register('mole', MoleViewSet)

mole_router = routers.NestedSimpleRouter(
    patient_router, r'mole', lookup='mole')
mole_router.register('image', MoleImageViewSet)

urlpatterns = [
    url(r'^', include(patient_router.urls)),
    url(r'^', include(mole_router.urls)),
]
