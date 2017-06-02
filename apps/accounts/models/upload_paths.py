import os

from skiniq.utils import get_timestamp


def photo_filepath(instance, filename):
    tstamp = get_timestamp()

    upload_filename, f_ext = os.path.splitext(filename)

    user_pk = instance.user.id
    new_filename = '{user_pk}_photo_{tstamp}{ext}'.format(
        user_pk=user_pk, tstamp=tstamp, ext=f_ext)

    return '/'.join(['users', str(user_pk), 'photo', new_filename])
