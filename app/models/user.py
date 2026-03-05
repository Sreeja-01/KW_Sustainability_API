"""
User model and authentication CRUD operations.
"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import Session, relationship
from sqlalchemy.exc import IntegrityError

from app.db.session import Base
from app.core.passwords import get_password_hash, verify_password
from app.schemas.user import UserCreate
from app.models.document import Document

class User(Base):
    __tablename__ = "users"

    # -------------------------
    # Primary Key
    # -------------------------
    id = Column(Integer, primary_key=True, index=True)

    # -------------------------
    # Authentication Fields
    # -------------------------
    email = Column(String, unique=True, index=True, nullable=False)

    hashed_password = Column(String, nullable=False)

    # -------------------------
    # User Status
    # -------------------------
    is_active = Column(Boolean, default=True)

    is_superuser = Column(Boolean, default=False)

    # -------------------------
    # Timestamps
    # -------------------------
    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # -------------------------
    # Relationships
    # -------------------------
    documents = relationship(
        "Document",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # -------------------------
    # Password verification
    # -------------------------
    def verify_password(self, password: str) -> bool:
        return verify_password(password, self.hashed_password)


# --------------------------------------------------
# CRUD FUNCTIONS
# --------------------------------------------------

def get_user_by_email(db: Session, email: str):
    """Retrieve user by email."""
    return db.query(User).filter(User.email == email).first()


def authenticate_user(db: Session, email: str, password: str):
    """Authenticate user credentials."""
    user = get_user_by_email(db, email)

    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user
from app.models.document import Document

def create_user(db: Session, user_create: UserCreate) -> User:
    """Create a new user."""
    try:
        hashed_password = get_password_hash(user_create.password)

        db_user = User(
            email=user_create.email,
            hashed_password=hashed_password,
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    except IntegrityError:
        db.rollback()
        raise ValueError("Email already registered")