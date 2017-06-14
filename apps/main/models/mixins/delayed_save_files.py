from django.db import models


class DelayedSaveFilesMixin(object):
    """
    Mixin delays saving files before instance will be saved.
    This might be useful if upload path depends on instance pk
    """
    def save(self, **kwargs):
        file_fields = {}
        is_new = not self.pk

        if is_new:
            for field in self._meta.fields:
                if isinstance(field, models.FileField):
                    field_name = field.name
                    file_fields[field_name] = getattr(self, field_name)
                    setattr(self, field_name, None)

        super(DelayedSaveFilesMixin, self).save(**kwargs)

        if is_new:
            for field_name, value in file_fields.items():
                setattr(self, field_name, value)
            self.save()
