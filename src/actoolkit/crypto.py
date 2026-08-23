from __future__ import annotations

import base64, json, os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from argon2.low_level import Type, hash_secret_raw

VERSION = 1
SALT_BYTES = 16
NONCE_BYTES = 12
KEY_BYTES = 32


def derive_key(password: str, salt: bytes, *, time_cost=3, memory_cost=65536, parallelism=4) -> bytes:
    if not isinstance(password, str) or not password:
        raise ValueError("password must be a non-empty string")
    if len(salt) != SALT_BYTES:
        raise ValueError("salt must be 16 bytes")
    return hash_secret_raw(password.encode(), salt, time_cost, memory_cost, parallelism, KEY_BYTES, Type.ID)


def encrypt_text(plaintext: str, password: str) -> str:
    if not isinstance(plaintext, str):
        raise TypeError("plaintext must be a string")
    salt = os.urandom(SALT_BYTES)
    nonce = os.urandom(NONCE_BYTES)
    key = derive_key(password, salt)
    aad = f"actoolkit:v{VERSION}".encode()
    ciphertext = AESGCM(key).encrypt(nonce, plaintext.encode(), aad)
    envelope = {"v": VERSION, "salt": base64.b64encode(salt).decode(), "nonce": base64.b64encode(nonce).decode(), "ct": base64.b64encode(ciphertext).decode()}
    return json.dumps(envelope, sort_keys=True, separators=(",", ":"))


def decrypt_text(token: str, password: str) -> str:
    try:
        env = json.loads(token)
        if env.get("v") != VERSION:
            raise ValueError("unsupported ciphertext version")
        salt = base64.b64decode(env["salt"], validate=True)
        nonce = base64.b64decode(env["nonce"], validate=True)
        ciphertext = base64.b64decode(env["ct"], validate=True)
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise ValueError("invalid ciphertext envelope") from exc
    if len(salt) != SALT_BYTES or len(nonce) != NONCE_BYTES or len(ciphertext) < 16:
        raise ValueError("invalid ciphertext dimensions")
    key = derive_key(password, salt)
    try:
        return AESGCM(key).decrypt(nonce, ciphertext, f"actoolkit:v{VERSION}".encode()).decode()
    except Exception as exc:
        raise ValueError("decryption failed") from exc
