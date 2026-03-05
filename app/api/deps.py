"""
API dependencies.

Provides:
- Database session
- Current authenticated user
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.db.session import SessionLocal
from app.core.config import settings
from app.models.user import get_user_by_email, User


# ---------------------------------------------------
# Database Dependency
# ---------------------------------------------------

def get_db():
    """
    Provide database session.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------
# JWT Bearer Authentication
# ---------------------------------------------------

security = HTTPBearer()


# ---------------------------------------------------
# Get Current User
# ---------------------------------------------------

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    Extract user from JWT token.
    """

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
        )

        email: str | None = payload.get("sub")

        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    user = get_user_by_email(db, email=email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user