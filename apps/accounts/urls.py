from django.conf.urls import url, include
from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token
from rest_framework_nested import routers
from djoser import views

from .viewsets import PatientViewSet, PatientConsentViewSet
from .views import current_user_view, sites_view, obtain_jwt_token


# This router mustn't have another viewsets because patient has nested routes
router_for_patients = routers.SimpleRouter()
router_for_patients.register('patient', PatientViewSet)

patient_router = routers.NestedSimpleRouter(
    router_for_patients, r'patient', lookup='patient')
patient_router.register('consent', PatientConsentViewSet)

urlpatterns = [
    url(r'^', include(router_for_patients.urls)),
    url(r'^', include(patient_router.urls)),

    url(r'^auth/current_user/$', current_user_view),
    url(r'^auth/sites/$', sites_view),

    # JWT authentication
    url(r'^auth/login/$', obtain_jwt_token),
    url(r'^auth/token-refresh/$', refresh_jwt_token),
    url(r'^auth/token-verify/$', verify_jwt_token),

    # Registration
    url(r'^auth/register/$', views.RegistrationView.as_view()),
    url(r'^auth/activate/$', views.ActivationView.as_view()),
    url(
        r'^auth/password/reset/$',
        views.PasswordResetView.as_view(),
    ),
    url(
        r'^auth/password/reset/confirm/$',
        views.PasswordResetConfirmView.as_view(),
    ),
]
