from datetime import datetime
from calendar import timegm

from rest_framework_jwt.settings import api_settings

from .serializers import DoctorSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    data = {
        'token': token,
    }

    if hasattr(user, 'doctor_role'):
        data.update({
            'doctor': DoctorSerializer(
                user.doctor_role,
                context={'request': request}
            ).data,
        })

    return data


def jwt_payload_handler(user):
    # TODO: use default payload handler after they release new version

    payload = {
        'user_id': user.pk,
        'username': user.username,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER

    return payload
