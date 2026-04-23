from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: str = "viewer"
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int  # change to str only if using UUID
    avatar_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


# 🔐 LOGIN REQUEST (this was missing)
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# � REGISTER REQUEST
class RegisterRequest(BaseModel):
    email: EmailStr
    name: str
    password: str


# �🔑 TOKEN RESPONSE
class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    user: UserRead


# 🔍 TOKEN DATA (decoded JWT)
class TokenData(BaseModel):
    sub: str
    jti: str
    role: str
    type: str