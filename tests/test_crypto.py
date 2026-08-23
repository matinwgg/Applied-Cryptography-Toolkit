import json
import pytest
from actoolkit.crypto import decrypt_text, encrypt_text


def test_round_trip():
    token = encrypt_text("confidential payment note", "correct horse battery staple")
    assert decrypt_text(token, "correct horse battery staple") == "confidential payment note"


def test_randomized_ciphertexts():
    a = encrypt_text("same", "password")
    b = encrypt_text("same", "password")
    assert a != b


def test_wrong_password_and_tampering_fail():
    token = encrypt_text("secret", "password")
    with pytest.raises(ValueError):
        decrypt_text(token, "wrong")
    env = json.loads(token)
    env["ct"] = env["ct"][:-2] + "AA"
    with pytest.raises(ValueError):
        decrypt_text(json.dumps(env), "password")
