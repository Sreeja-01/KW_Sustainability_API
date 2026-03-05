# app/core/passwords.py
"""Password hashing and verification utilities (pbkdf2_sha256)."""

from passlib.hash import pbkdf2_sha256


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against stored hash."""
    return pbkdf2_sha256.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash plain password using pbkdf2_sha256."""
    return pbkdf2_sha256.hash(password)
