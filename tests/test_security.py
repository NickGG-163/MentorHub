import os
from datetime import datetime, timedelta, timezone

import jwt
import pytest

from mentorhub.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_hashing():
    hashed = hash_password("qwerty123")

    assert verify_password("qwerty123", hashed) is True
    assert verify_password("qwerty12", hashed) is False
    assert hashed != "qwerty123"


def test_decoding_access_token():
    token = create_access_token(123)
    decode_token = decode_access_token(token)

    assert decode_token == 123


def test_expired_token():
    payload = {
        "sub": "123",
        "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
    }

    token = jwt.encode(
        payload,
        os.environ["JWT_SECRET_KEY"],
        algorithm="HS256",
    )

    with pytest.raises(jwt.ExpiredSignatureError):
        decode_access_token(token)


def test_invalid_signature():
    payload = {
        "sub": "123",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }

    token = jwt.encode(
        payload,
        "another-secret-key",
        algorithm="HS256",
    )

    with pytest.raises(jwt.InvalidSignatureError):
        decode_access_token(token)
