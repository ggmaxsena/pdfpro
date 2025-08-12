from django.apps import AppConfig


class TravelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.travel'

    def ready(self):
        # Importar modelos para que o Django os detecte
        from .infrastructure import models
