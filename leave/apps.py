from django.apps import AppConfig
import os
from dotenv import load_dotenv



class Settonfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'leave'

    def ready(self):
        from .models import AppSettings
        from django.db.utils import OperationalError
        try:
            AppSettings.objects.get_or_create(pk=1)
        except OperationalError:
            pass