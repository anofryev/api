from django.apps import AppConfig


class MolesConfig(AppConfig):
    name = 'apps.moles'

    def ready(self):
        from . import signals  # noqa
