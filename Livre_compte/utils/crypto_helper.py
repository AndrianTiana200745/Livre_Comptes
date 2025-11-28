# utils/crypto_helper.py
import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

# Dérive une clé 32 bytes à partir d'un mot de passe et d'un sel
def derive_key_from_password(password: str, salt: bytes = None) -> tuple[bytes, bytes]:
    """
    Retourne (key, salt). Si salt == None, on génère un sel aléatoire.
    Stocke le sel (non secret) dans la config/db pour pouvoir dériver la même clé.
    """
    if salt is None:
        salt = os.urandom(16)
    password_bytes = password.encode('utf-8')
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200_000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
    return key, salt

def encrypt_text(plaintext: str, fernet_key: bytes) -> bytes:
    f = Fernet(fernet_key)
    return f.encrypt(plaintext.encode('utf-8'))

def decrypt_text(token: bytes, fernet_key: bytes) -> str:
    f = Fernet(fernet_key)
    return f.decrypt(token).decode('utf-8')

