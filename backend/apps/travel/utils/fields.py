from django.db import models
from django.db.models import Field
from .encryption import encrypt_data, decrypt_data

class EncryptedCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value is None:
            return value
        return encrypt_data(value)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return decrypt_data(value)

    def to_python(self, value):
        if isinstance(value, str) and value.startswith('gAAAAA'): # Heuristic to check if it's encrypted
            return decrypt_data(value)
        return value
