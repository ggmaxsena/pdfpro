
from django.db import models
from django.conf import settings

class AnonimizationLog(models.Model):
    """
    Modelo para registrar logs de anonimização de arquivos.
    """
    user: models.ForeignKey = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file_name: models.CharField = models.CharField(max_length=255)
    timestamp: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    sheet_names = models.JSONField()

    def __str__(self):
        """
        Retorna a representação em string do log de anonimização.
        """
        return f'{self.user.email} - {self.file_name}'
