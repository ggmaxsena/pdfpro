
from django.db import models
from django.conf import settings

class AnonimizationLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    sheet_names = models.JSONField()

    def __str__(self):
        return f'{self.user.email} - {self.file_name}'
