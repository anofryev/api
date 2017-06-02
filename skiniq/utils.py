import time


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
    }


def get_timestamp():
    return int(time.time())
