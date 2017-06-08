from django.test import mock

from .api_test_case import APITestCase


def patch(target, **kwargs):
    if 'new_callable' not in kwargs and 'autospec' not in kwargs:
        kwargs['autospec'] = True
    return mock.patch(target, **kwargs)
