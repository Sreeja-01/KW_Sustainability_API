"""Auth schemas."""
from pydantic import BaseModel
from typing import Optional
from app.schemas.user import UserOut

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    user: UserOut
    access_token: str
