from django.conf import settings
from django.utils.functional import LazyObject
from django.core.files.storage import DefaultStorage
from storages.backends.s3boto import S3BotoStorage


class PublicStorage(LazyObject):
    def _setup(self):
        storage = DefaultStorage()

        public_bucket = settings.AWS_STORAGE_PUBLIC_BUCKET_NAME
        if public_bucket:  # pragma: no cover
            storage = S3BotoStorage(
                bucket=public_bucket, querystring_auth=False)

        self._wrapped = storage


public_storage = PublicStorage()
