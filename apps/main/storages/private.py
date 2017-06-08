from django.conf import settings
from django.utils.functional import LazyObject
from django.core.files.storage import DefaultStorage
from storages.backends.s3boto import S3BotoStorage


class PrivateStorage(LazyObject):
    def _setup(self):
        storage = DefaultStorage()

        private_bucket = settings.AWS_STORAGE_BUCKET_NAME
        if private_bucket:
            storage = S3BotoStorage(bucket=private_bucket)

        self._wrapped = storage


private_storage = PrivateStorage()
