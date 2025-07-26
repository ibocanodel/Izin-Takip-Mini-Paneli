from django.apps import AppConfig


class Settonfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'leave'

    def ready(self):
        from django.db.utils import OperationalError

        from .models import AppSettings
        try:
            AppSettings.objects.get_or_create(pk=1)
        except OperationalError:
            pass