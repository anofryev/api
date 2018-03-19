import os

from sorl.thumbnail import get_thumbnail


IMAGE_EXTENSIONS = [
    'jpg', 'jpeg', 'tiff', 'tif', 'r3d', 'ari', 'gif', 'bmp', 'png']


class ThumbnailMixin(object):

    ATTACHMENT_FIELD_NAME = 'attachment'

    @property
    def attachment(self):
        if not hasattr(self, self.ATTACHMENT_FIELD_NAME):
            raise NotImplementedError('you need to define attachment field')

        return getattr(self, self.ATTACHMENT_FIELD_NAME)

    @property
    def attachment_name(self):
        return os.path.basename(self.attachment.name) if self.attachment else ''

    @property
    def extension(self):
        return self.attachment_name.split('.')[-1].lower()

    @property
    def thumbnail(self):
        if self.attachment is None or self.extension not in IMAGE_EXTENSIONS:
            return None

        try:
            return get_thumbnail(self.attachment, '100x100', crop='center',
                                 quality=99, format='PNG')
        except Exception:
            raise
