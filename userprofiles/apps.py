from django.apps import AppConfig


class UserprofilesConfig(AppConfig):
    name = 'userprofiles'

    def ready(self):
        import userprofiles.signals