"""
Authentication routes.
Handles user registration and login.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.user import create_user, authenticate_user
from app.schemas.user import UserCreate, UserLogin
from app.core.security import create_access_token

router = APIRouter()


# ---------------------------------------------------------
# Register
# ---------------------------------------------------------

@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Register a new user and return JWT token.
    """

    try:
        new_user = create_user(db, user)

        token = create_access_token(
            data={"sub": new_user.email}
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": new_user.id,
                "email": new_user.email,
                "is_active": new_user.is_active,
                "is_superuser": new_user.is_superuser,
            },
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ---------------------------------------------------------
# Login
# ---------------------------------------------------------

@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    """
    Login user and return JWT token.
    """

    db_user = authenticate_user(db, user.email, user.password)

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    token = create_access_token(
        data={"sub": db_user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "email": db_user.email,
            "is_active": db_user.is_active,
            "is_superuser": db_user.is_superuser,
        },
    }