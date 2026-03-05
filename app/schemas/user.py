"""
User schemas for request and response validation.
"""

from pydantic import BaseModel, EmailStr


# ---------------------------------------------------
# Base schema
# ---------------------------------------------------

class UserBase(BaseModel):
    email: EmailStr


# ---------------------------------------------------
# User creation schema
# ---------------------------------------------------

class UserCreate(UserBase):
    password: str


# ---------------------------------------------------
# Login schema
# ---------------------------------------------------

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ---------------------------------------------------
# User response schema
# ---------------------------------------------------

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True


# ---------------------------------------------------
# Auth response schema
# ---------------------------------------------------

class AuthResponse(BaseModel):
    user: UserResponse
    access_token: str