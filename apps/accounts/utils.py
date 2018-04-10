from datetime import datetime

from rest_framework_jwt.settings import api_settings

from .serializers import DoctorFullSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    data = {
        'token': token,
        'doctor': DoctorFullSerializer(
            user.doctor_role,
            context={'request': request}
        ).data,
    }

    return data


def jwt_payload_handler(user):
    # TODO: use default payload handler after they release new version

    payload = {
        'user_id': user.pk,
        'username': user.username,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }

    return payload
