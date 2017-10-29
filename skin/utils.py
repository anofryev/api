import os
import time


def get_timestamp():
    return int(time.time())


def generate_filename(source_filename, prefix):
    tstamp = get_timestamp()

    _, f_ext = os.path.splitext(source_filename)

    return '{prefix}_{tstamp}{ext}'.format(
        prefix=prefix, tstamp=tstamp, ext=f_ext)
