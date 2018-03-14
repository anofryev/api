from django.conf.urls import url, include
from rest_framework_jwt.views import (
    obtain_jwt_token, refresh_jwt_token, verify_jwt_token, )
from rest_framework_nested import routers
from djoser import views

from .viewsets import (PatientViewSet, PatientConsentViewSet,
                       SiteJoinRequestViewSet, )
from .views import (
    current_user_view, sites_view, reset_confirmation_view,
    register_as_patient_view)


# This router mustn't have another viewsets because patient has nested routes
router_for_patients = routers.SimpleRouter()
router_for_patients.register('patient', PatientViewSet)

patient_router = routers.NestedSimpleRouter(
    router_for_patients, r'patient', lookup='patient')
patient_router.register('consent', PatientConsentViewSet)

router_for_doctors = routers.SimpleRouter()
router_for_doctors.register('site_join_requests',
                            SiteJoinRequestViewSet)

urlpatterns = [
    url(r'^', include(router_for_patients.urls)),
    url(r'^', include(patient_router.urls)),
    url(r'^', include(router_for_doctors.urls)),

    url(r'^auth/current_user/$', current_user_view),
    url(r'^auth/sites/$', sites_view),

    # JWT authentication
    url(r'^auth/login/$', obtain_jwt_token),
    url(r'^auth/token-refresh/$', refresh_jwt_token),
    url(r'^auth/token-verify/$', verify_jwt_token),

    # Registration
    url(r'^auth/register/$', views.UserCreateView.as_view()),
    url(r'^auth/register_as_patient/$', register_as_patient_view),
    url(r'^auth/activate/$', views.ActivationView.as_view()),
    url(
        r'^auth/password/reset/$',
        views.PasswordResetView.as_view(),
    ),
    url(
        r'^auth/password/reset/confirm/$',
        reset_confirmation_view,
    ),
]
