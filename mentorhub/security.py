import os
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hasher.verify(password, hashed_password)


def create_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
    }
    return jwt.encode(payload, os.environ["JWT_SECRET_KEY"], algorithm="HS256")


def decode_access_token(token: str) -> int:
    payload = jwt.decode(token, os.environ["JWT_SECRET_KEY"], algorithms=[
                         "HS256"], options={"require": ["sub", "exp"]})
    return int(payload["sub"])

