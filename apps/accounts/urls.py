from django.conf.urls import url
from django.contrib.auth import views as auth_views
from rest_framework_jwt.views import (
    obtain_jwt_token, refresh_jwt_token, verify_jwt_token)
from rest_framework import routers

from .views import *
from .viewsets import *


router = routers.SimpleRouter()

urlpatterns = [
    url(r'^auth/login/', obtain_jwt_token),
    url(r'^auth/token-refresh/', refresh_jwt_token),
    url(r'^auth/token-verify/', verify_jwt_token),

    url(r'^auth/password_reset/$', user_password_reset_view),
    url(r'^auth/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^auth/reset/done/$',
        auth_views.password_reset_complete,
        name='password_reset_complete'),
]

urlpatterns += router.urls
