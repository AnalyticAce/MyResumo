from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import List, Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str | None] = None

class User(BaseModel):
    username: str = Field(..., example="johndoe")
    email: Optional[EmailStr] = Field(None, example="johndoe@gmail.com")
    disabled: Optional[bool] = False
    provider: Optional[str] = "github"
    profile_picture: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(datetime.timezone.utc))

class UserInDB(User):
    hashed_password: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    
class FormData(BaseModel):
    job_description: Optional[str] = None
    resume_text: Optional[str] = None
    resume_tone: Optional[str] = None
    resume_language: Optional[str] = None
    section_arrange: Optional[List[str]] = None

class Resume(BaseModel):
    template_id: Optional[str] = None
    job_description: Optional[str] = None
    resume_data: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(datetime.timezone.utc))