from __future__ import annotations

import base64
import json
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from argon2.low_level import Type, hash_secret_raw

VERSION = 1
SALT_BYTES = 16
NONCE_BYTES = 12
KEY_BYTES = 32
MIN_PASSWORD_BYTES = 8


def derive_key(password: str, salt: bytes, *, time_cost=3, memory_cost=65536, parallelism=4) -> bytes:
    if not isinstance(password, str) or not password:
        raise ValueError("password must be a non-empty string")
    if len(password.encode("utf-8")) < MIN_PASSWORD_BYTES:
        raise ValueError("password must be at least 8 UTF-8 bytes")
    if not isinstance(salt, bytes) or len(salt) != SALT_BYTES:
        raise ValueError("salt must be 16 bytes")
    if not (1 <= time_cost <= 10 and 8 <= memory_cost <= 2_097_152 and 1 <= parallelism <= 16):
        raise ValueError("invalid Argon2id parameters")
    return hash_secret_raw(password.encode("utf-8"), salt, time_cost, memory_cost, parallelism, KEY_BYTES, Type.ID)


def encrypt_text(plaintext: str, password: str) -> str:
    if not isinstance(plaintext, str):
        raise TypeError("plaintext must be a string")
    salt = os.urandom(SALT_BYTES)
    nonce = os.urandom(NONCE_BYTES)
    key = derive_key(password, salt)
    aad = f"actoolkit:v{VERSION}".encode("ascii")
    ciphertext = AESGCM(key).encrypt(nonce, plaintext.encode("utf-8"), aad)
    envelope = {"v": VERSION, "salt": base64.b64encode(salt).decode("ascii"), "nonce": base64.b64encode(nonce).decode("ascii"), "ct": base64.b64encode(ciphertext).decode("ascii")}
    return json.dumps(envelope, sort_keys=True, separators=(",", ":"))


def decrypt_text(token: str, password: str) -> str:
    try:
        if not isinstance(token, str) or len(token) > 16 * 1024 * 1024:
            raise ValueError("invalid ciphertext envelope")
        env = json.loads(token)
        if not isinstance(env, dict) or env.get("v") != VERSION:
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
        plaintext = AESGCM(key).decrypt(nonce, ciphertext, f"actoolkit:v{VERSION}".encode("ascii"))
        return plaintext.decode("utf-8")
    except Exception as exc:
        raise ValueError("decryption failed") from exc
