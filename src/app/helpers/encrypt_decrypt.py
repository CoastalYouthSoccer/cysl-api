import hmac
import hashlib
from cryptography.fernet import Fernet
from app.config import get_settings

config = get_settings()


fernet = Fernet(config.db_encryption_key.encode())

def encrypt(value: str) -> str:
    return fernet.encrypt(value.encode()).decode()

def decrypt(value: str) -> str:
    return fernet.decrypt(value.encode()).decode()

def hmac_value(value: str) -> str:
    return hmac.new(config.hmac_secret)
