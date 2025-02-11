from enum import Enum
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    full_name: Optional[str | None] = None

class User(BaseModel):
    full_name: str = Field(..., example="johndoe")
    email: Optional[EmailStr] = Field(None, example="johndoe@gmail.com")
    disabled: Optional[bool] = False
    provider: Optional[str] = "github"
    profile_picture: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserInDB(User):
    hashed_password: Optional[str] = None

class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str