import logging
import re

class SensitiveDataFilter(logging.Filter):
    def filter(self, record):
        message = record.getMessage()

        # Máscara de CPF (XXX.XXX.XXX-XX)
        # Procura por padrões de CPF com ou sem pontuação
        message = re.sub(r'\b(\d{3}\.?\d{3}\.?\d{3}-?)(\d{2})\b', r'***.***.***-\2', message)

        # Máscara de Conta Bancária (apenas números, mantém os últimos 4 dígitos)
        # Procura por sequências de dígitos que podem ser contas bancárias
        message = re.sub(r'\b(\d+)(\d{4})\b', r'********\2', message)

        record.msg = message
        return True
