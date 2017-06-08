from django.conf.urls import url, include
from rest_framework_jwt.views import (
    obtain_jwt_token, refresh_jwt_token, verify_jwt_token)
from rest_framework import routers

from .viewsets import *


# This router mustn't have another viewsets because patient has nested routes
router_for_patients = routers.SimpleRouter()
router_for_patients.register('patient', PatientViewSet)

urlpatterns = [
    url(r'^', include(router_for_patients.urls)),

    # JWT authentication
    url(r'^auth/login/', obtain_jwt_token),
    url(r'^auth/token-refresh/', refresh_jwt_token),
    url(r'^auth/token-verify/', verify_jwt_token),
]
