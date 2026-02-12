import os
from cryptography.fernet import Fernet

def _get_fernet() -> Fernet:
    key = os.getenv("FERNET_KEY")
    if not key:
        raise RuntimeError("FERNET_KEY is not set in environment (.env)")
    return Fernet(key.encode("utf-8"))

def encrypt_str(value: str) -> str:
    f = _get_fernet()
    token = f.encrypt(value.encode("utf-8"))
    return token.decode("utf-8")

def mask_document(doc_digits: str) -> str:
    last4 = doc_digits[-4:] if doc_digits else ""
    return "*" * (max(len(doc_digits) - 4, 0)) + last4
