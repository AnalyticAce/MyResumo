from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import List, Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str | None] = None
    
    @field_validator('username')
    def validate_username(cls, value):
        if len(value) < 3 or len(value) > 50:
            raise ValueError('username must be between 3 and 50 characters')
        return value

class User(BaseModel):
    username: str = Field(..., example="johndoe")
    email: Optional[EmailStr] = Field(None, example="johndoe@gmail.com")
    disabled: Optional[bool] = False
    provider: Optional[str] = "github"
    profile_picture: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(datetime.timezone.utc))

    @field_validator('username')
    def validate_username(cls, value):
        if len(value) < 3 or len(value) > 50:
            raise ValueError('username must be between 3 and 50 characters')
        if not value.isalnum():
            raise ValueError('username must be alphanumeric')
        return value

    @field_validator('provider')
    def validate_provider(cls, value):
        valid_providers = ['github', 'google']
        if value and value.lower() not in valid_providers:
            raise ValueError('provider must be one of: github, google')
        return value

    @field_validator('profile_picture')
    def validate_profile_picture(cls, value):
        if value and not value.startswith(('http://', 'https://')):
            raise ValueError('profile_picture must be a valid URL')
        return value

    @field_validator('created_at')
    def validate_created_at(cls, value):
        if value > datetime.now(datetime.timezone.utc):
            raise ValueError('created_at cannot be in the future')
        return value

class UserInDB(User):
    hashed_password: Optional[str] = None

class FormData(BaseModel):
    job_description: Optional[str] = None
    resume_text: Optional[str] = None
    resume_tone: Optional[str] = None
    resume_language: Optional[str] = None
    section_arrange: Optional[List[str]] = None

    @field_validator('job_description')
    def validate_job_description(cls, value):
        if value and len(value) < 10:
            raise ValueError('job_description must be at least 10 characters long')
        return value

    @field_validator('resume_text')
    def validate_resume_text(cls, value):
        if value and len(value) < 50:
            raise ValueError('resume_text must be at least 50 characters long')
        return value

    @field_validator('resume_tone')
    def validate_resume_tone(cls, value):
        valid_tones = ['professional', 'casual', 'formal', 'friendly']
        if value and value.lower() not in valid_tones:
            raise ValueError('resume_tone must be one of: professional, casual, formal, friendly')
        return value

    @field_validator('resume_language')
    def validate_resume_language(cls, value):
        valid_languages = ['en', 'es', 'fr', 'de']
        if value and value.lower() not in valid_languages:
            raise ValueError('resume_language must be one of: en, es, fr, de')
        return value

    @field_validator('section_arrange')
    def validate_section_arrange(cls, value):
        if value and not all(isinstance(item, str) for item in value):
            raise ValueError('all items in section_arrange must be strings')
        return value

class Resume(BaseModel):
    user_id: Optional[str] = None
    template_id: Optional[str] = None
    job_description: Optional[str] = None
    resume_data: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(datetime.timezone.utc))

    @field_validator('template_id')
    def validate_template_id(cls, value):
        if value and not value.isalnum():
            raise ValueError('template_id must be alphanumeric')
        return value

    @field_validator('job_description')
    def validate_job_description(cls, value):
        if value and len(value) < 10:
            raise ValueError('job_description must be at least 10 characters long')
        return value

    @field_validator('resume_data')
    def validate_resume_data(cls, value):
        if value and len(value) < 50:
            raise ValueError('resume_data must be at least 50 characters long')
        return value

    @field_validator('created_at')
    def validate_created_at(cls, value):
        if value > datetime.now(datetime.timezone.utc):
            raise ValueError('created_at cannot be in the future')
        return value