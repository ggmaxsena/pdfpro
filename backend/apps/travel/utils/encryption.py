from cryptography.fernet import Fernet
from decouple import config

# Obtenha a chave de criptografia das variáveis de ambiente
# Em produção, esta chave deve ser gerenciada de forma segura (ex: HashiCorp Vault, AWS KMS)
ENCRYPTION_KEY = config('ENCRYPTION_KEY').encode('utf-8')

fernet = Fernet(ENCRYPTION_KEY)

def encrypt_data(data: str) -> str:
    """Criptografa uma string."""
    return fernet.encrypt(data.encode('utf-8')).decode('utf-8')

def decrypt_data(encrypted_data: str) -> str:
    """Descriptografa uma string."""
    return fernet.decrypt(encrypted_data.encode('utf-8')).decode('utf-8')
